from __future__ import unicode_literals

import errno
import re
import io
import binascii
try:
    from Crypto.Cipher import AES
    can_decrypt_frag = True
except ImportError:
    can_decrypt_frag = False
try:
    import concurrent.futures
    can_threaded_download = True
except ImportError:
    can_threaded_download = False

from ..downloader import _get_real_downloader
from .fragment import FragmentFD
from .external import FFmpegFD

from ..compat import (
    compat_urllib_error,
    compat_urlparse,
    compat_struct_pack,
)
from ..utils import (
    parse_m3u8_attributes,
    sanitize_open,
    update_url_query,
    bug_reports_message,
)
from .. import webvtt


class HlsFD(FragmentFD):
    """
    Download segments in a m3u8 manifest. External downloaders can take over
    the fragment downloads by supporting the 'm3u8_frag_urls' protocol and
    re-defining 'supports_manifest' function
    """

    FD_NAME = 'hlsnative'

    @staticmethod
    def can_download(manifest, info_dict, allow_unplayable_formats=False, with_crypto=can_decrypt_frag):
        UNSUPPORTED_FEATURES = [
            # r'#EXT-X-BYTERANGE',  # playlists composed of byte ranges of media files [2]

            # Live streams heuristic does not always work (e.g. geo restricted to Germany
            # http://hls-geo.daserste.de/i/videoportal/Film/c_620000/622873/format,716451,716457,716450,716458,716459,.mp4.csmil/index_4_av.m3u8?null=0)
            # r'#EXT-X-MEDIA-SEQUENCE:(?!0$)',  # live streams [3]

            # This heuristic also is not correct since segments may not be appended as well.
            # Twitch vods of finished streams have EXT-X-PLAYLIST-TYPE:EVENT despite
            # no segments will definitely be appended to the end of the playlist.
            # r'#EXT-X-PLAYLIST-TYPE:EVENT',  # media segments may be appended to the end of
            #                                 # event media playlists [4]
            # r'#EXT-X-MAP:',  # media initialization [5]
            # 1. https://tools.ietf.org/html/draft-pantos-http-live-streaming-17#section-4.3.2.4
            # 2. https://tools.ietf.org/html/draft-pantos-http-live-streaming-17#section-4.3.2.2
            # 3. https://tools.ietf.org/html/draft-pantos-http-live-streaming-17#section-4.3.3.2
            # 4. https://tools.ietf.org/html/draft-pantos-http-live-streaming-17#section-4.3.3.5
            # 5. https://tools.ietf.org/html/draft-pantos-http-live-streaming-17#section-4.3.2.5
        ]
        if not allow_unplayable_formats:
            UNSUPPORTED_FEATURES += [
                r'#EXT-X-KEY:METHOD=(?!NONE|AES-128)',  # encrypted streams [1]
            ]

        def check_results():
            yield not info_dict.get('is_live')
            is_aes128_enc = '#EXT-X-KEY:METHOD=AES-128' in manifest
            yield with_crypto or not is_aes128_enc
            yield not (is_aes128_enc and r'#EXT-X-BYTERANGE' in manifest)
            for feature in UNSUPPORTED_FEATURES:
                yield not re.search(feature, manifest)
        return all(check_results())

    def real_download(self, filename, info_dict):
        man_url = info_dict['url']
        self.to_screen('[%s] Downloading m3u8 manifest' % self.FD_NAME)

        urlh = self.ydl.urlopen(self._prepare_url(info_dict, man_url))
        man_url = urlh.geturl()
        s = urlh.read().decode('utf-8', 'ignore')

        if not self.can_download(s, info_dict, self.params.get('allow_unplayable_formats')):
            if info_dict.get('extra_param_to_segment_url') or info_dict.get('_decryption_key_url'):
                self.report_error('pycryptodome not found. Please install')
                return False
            if self.can_download(s, info_dict, with_crypto=True):
                self.report_warning('pycryptodome is needed to download this file natively')
            fd = FFmpegFD(self.ydl, self.params)
            self.report_warning(
                '%s detected unsupported features; extraction will be delegated to %s' % (self.FD_NAME, fd.get_basename()))
            # TODO: Make progress updates work without hooking twice
            # for ph in self._progress_hooks:
            #     fd.add_progress_hook(ph)
            return fd.real_download(filename, info_dict)

        is_webvtt = info_dict['ext'] == 'vtt'
        if is_webvtt:
            real_downloader = None  # Packing the fragments is not currently supported for external downloader
        else:
            real_downloader = _get_real_downloader(info_dict, 'm3u8_frag_urls', self.params, None)
        if real_downloader and not real_downloader.supports_manifest(s):
            real_downloader = None
        if real_downloader:
            self.to_screen(
                '[%s] Fragment downloads will be delegated to %s' % (self.FD_NAME, real_downloader.get_basename()))

        def is_ad_fragment_start(s):
            return (s.startswith('#ANVATO-SEGMENT-INFO') and 'type=ad' in s
                    or s.startswith('#UPLYNK-SEGMENT') and s.endswith(',ad'))

        def is_ad_fragment_end(s):
            return (s.startswith('#ANVATO-SEGMENT-INFO') and 'type=master' in s
                    or s.startswith('#UPLYNK-SEGMENT') and s.endswith(',segment'))

        fragments = []

        media_frags = 0
        ad_frags = 0
        ad_frag_next = False
        for line in s.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                if is_ad_fragment_start(line):
                    ad_frag_next = True
                elif is_ad_fragment_end(line):
                    ad_frag_next = False
                continue
            if ad_frag_next:
                ad_frags += 1
                continue
            media_frags += 1

        ctx = {
            'filename': filename,
            'total_frags': media_frags,
            'ad_frags': ad_frags,
        }

        if real_downloader:
            self._prepare_external_frag_download(ctx)
        else:
            self._prepare_and_start_frag_download(ctx)

        extra_state = ctx.setdefault('extra_state', {})

        fragment_retries = self.params.get('fragment_retries', 0)
        skip_unavailable_fragments = self.params.get('skip_unavailable_fragments', True)
        test = self.params.get('test', False)

        format_index = info_dict.get('format_index')
        extra_query = None
        extra_param_to_segment_url = info_dict.get('extra_param_to_segment_url')
        if extra_param_to_segment_url:
            extra_query = compat_urlparse.parse_qs(extra_param_to_segment_url)
        i = 0
        media_sequence = 0
        decrypt_info = {'METHOD': 'NONE'}
        byte_range = {}
        discontinuity_count = 0
        frag_index = 0
        ad_frag_next = False
        for line in s.splitlines():
            line = line.strip()
            if line:
                if not line.startswith('#'):
                    if format_index and discontinuity_count != format_index:
                        continue
                    if ad_frag_next:
                        continue
                    frag_index += 1
                    if frag_index <= ctx['fragment_index']:
                        continue
                    frag_url = (
                        line
                        if re.match(r'^https?://', line)
                        else compat_urlparse.urljoin(man_url, line))
                    if extra_query:
                        frag_url = update_url_query(frag_url, extra_query)

                    fragments.append({
                        'frag_index': frag_index,
                        'url': frag_url,
                        'decrypt_info': decrypt_info,
                        'byte_range': byte_range,
                        'media_sequence': media_sequence,
                    })

                elif line.startswith('#EXT-X-MAP'):
                    if format_index and discontinuity_count != format_index:
                        continue
                    if frag_index > 0:
                        self.report_error(
                            'Initialization fragment found after media fragments, unable to download')
                        return False
                    frag_index += 1
                    map_info = parse_m3u8_attributes(line[11:])
                    frag_url = (
                        map_info.get('URI')
                        if re.match(r'^https?://', map_info.get('URI'))
                        else compat_urlparse.urljoin(man_url, map_info.get('URI')))
                    if extra_query:
                        frag_url = update_url_query(frag_url, extra_query)

                    fragments.append({
                        'frag_index': frag_index,
                        'url': frag_url,
                        'decrypt_info': decrypt_info,
                        'byte_range': byte_range,
                        'media_sequence': media_sequence
                    })

                    if map_info.get('BYTERANGE'):
                        splitted_byte_range = map_info.get('BYTERANGE').split('@')
                        sub_range_start = int(splitted_byte_range[1]) if len(splitted_byte_range) == 2 else byte_range['end']
                        byte_range = {
                            'start': sub_range_start,
                            'end': sub_range_start + int(splitted_byte_range[0]),
                        }

                elif line.startswith('#EXT-X-KEY'):
                    decrypt_url = decrypt_info.get('URI')
                    decrypt_info = parse_m3u8_attributes(line[11:])
                    if decrypt_info['METHOD'] == 'AES-128':
                        if 'IV' in decrypt_info:
                            decrypt_info['IV'] = binascii.unhexlify(decrypt_info['IV'][2:].zfill(32))
                        if not re.match(r'^https?://', decrypt_info['URI']):
                            decrypt_info['URI'] = compat_urlparse.urljoin(
                                man_url, decrypt_info['URI'])
                        if extra_query:
                            decrypt_info['URI'] = update_url_query(decrypt_info['URI'], extra_query)
                        if decrypt_url != decrypt_info['URI']:
                            decrypt_info['KEY'] = None

                elif line.startswith('#EXT-X-MEDIA-SEQUENCE'):
                    media_sequence = int(line[22:])
                elif line.startswith('#EXT-X-BYTERANGE'):
                    splitted_byte_range = line[17:].split('@')
                    sub_range_start = int(splitted_byte_range[1]) if len(splitted_byte_range) == 2 else byte_range['end']
                    byte_range = {
                        'start': sub_range_start,
                        'end': sub_range_start + int(splitted_byte_range[0]),
                    }
                elif is_ad_fragment_start(line):
                    ad_frag_next = True
                elif is_ad_fragment_end(line):
                    ad_frag_next = False
                elif line.startswith('#EXT-X-DISCONTINUITY'):
                    discontinuity_count += 1
                i += 1
                media_sequence += 1

        # We only download the first fragment during the test
        if test:
            fragments = [fragments[0] if fragments else None]

        if real_downloader:
            info_copy = info_dict.copy()
            info_copy['fragments'] = fragments
            fd = real_downloader(self.ydl, self.params)
            # TODO: Make progress updates work without hooking twice
            # for ph in self._progress_hooks:
            #     fd.add_progress_hook(ph)
            success = fd.real_download(filename, info_copy)
            if not success:
                return False
        else:
            def decrypt_fragment(fragment, frag_content):
                decrypt_info = fragment['decrypt_info']
                if decrypt_info['METHOD'] != 'AES-128':
                    return frag_content
                iv = decrypt_info.get('IV') or compat_struct_pack('>8xq', fragment['media_sequence'])
                decrypt_info['KEY'] = decrypt_info.get('KEY') or self.ydl.urlopen(
                    self._prepare_url(info_dict, info_dict.get('_decryption_key_url') or decrypt_info['URI'])).read()
                # Don't decrypt the content in tests since the data is explicitly truncated and it's not to a valid block
                # size (see https://github.com/ytdl-org/youtube-dl/pull/27660). Tests only care that the correct data downloaded,
                # not what it decrypts to.
                if test:
                    return frag_content
                return AES.new(decrypt_info['KEY'], AES.MODE_CBC, iv).decrypt(frag_content)

            def download_fragment(fragment):
                frag_index = fragment['frag_index']
                frag_url = fragment['url']
                byte_range = fragment['byte_range']

                ctx['fragment_index'] = frag_index

                count = 0
                headers = info_dict.get('http_headers', {})
                if byte_range:
                    headers['Range'] = 'bytes=%d-%d' % (byte_range['start'], byte_range['end'] - 1)
                while count <= fragment_retries:
                    try:
                        success, frag_content = self._download_fragment(
                            ctx, frag_url, info_dict, headers)
                        if not success:
                            return False, frag_index
                        break
                    except compat_urllib_error.HTTPError as err:
                        # Unavailable (possibly temporary) fragments may be served.
                        # First we try to retry then either skip or abort.
                        # See https://github.com/ytdl-org/youtube-dl/issues/10165,
                        # https://github.com/ytdl-org/youtube-dl/issues/10448).
                        count += 1
                        if count <= fragment_retries:
                            self.report_retry_fragment(err, frag_index, count, fragment_retries)
                if count > fragment_retries:
                    ctx['dest_stream'].close()
                    self.report_error('Giving up after %s fragment retries' % fragment_retries)
                    return False, frag_index

                return decrypt_fragment(fragment, frag_content), frag_index

            pack_fragment = lambda frag_content, _: frag_content

            if is_webvtt:
                def pack_fragment(frag_content, frag_index):
                    output = io.StringIO()
                    adjust = 0
                    for block in webvtt.parse_fragment(frag_content):
                        if isinstance(block, webvtt.CueBlock):
                            block.start += adjust
                            block.end += adjust

                            dedup_window = extra_state.setdefault('webvtt_dedup_window', [])
                            cue = block.as_json

                            # skip the cue if an identical one appears
                            # in the window of potential duplicates
                            # and prune the window of unviable candidates
                            i = 0
                            skip = True
                            while i < len(dedup_window):
                                window_cue = dedup_window[i]
                                if window_cue == cue:
                                    break
                                if window_cue['end'] >= cue['start']:
                                    i += 1
                                    continue
                                del dedup_window[i]
                            else:
                                skip = False

                            if skip:
                                continue

                            # add the cue to the window
                            dedup_window.append(cue)
                        elif isinstance(block, webvtt.Magic):
                            # take care of MPEG PES timestamp overflow
                            if block.mpegts is None:
                                block.mpegts = 0
                            extra_state.setdefault('webvtt_mpegts_adjust', 0)
                            block.mpegts += extra_state['webvtt_mpegts_adjust'] << 33
                            if block.mpegts < extra_state.get('webvtt_mpegts_last', 0):
                                extra_state['webvtt_mpegts_adjust'] += 1
                                block.mpegts += 1 << 33
                            extra_state['webvtt_mpegts_last'] = block.mpegts

                            if frag_index == 1:
                                extra_state['webvtt_mpegts'] = block.mpegts or 0
                                extra_state['webvtt_local'] = block.local or 0
                                # XXX: block.local = block.mpegts = None ?
                            else:
                                if block.mpegts is not None and block.local is not None:
                                    adjust = (
                                        (block.mpegts - extra_state.get('webvtt_mpegts', 0))
                                        - (block.local - extra_state.get('webvtt_local', 0))
                                    )
                                continue
                        elif isinstance(block, webvtt.HeaderBlock):
                            if frag_index != 1:
                                # XXX: this should probably be silent as well
                                # or verify that all segments contain the same data
                                self.report_warning(bug_reports_message(
                                    'Discarding a %s block found in the middle of the stream; '
                                    'if the subtitles display incorrectly,'
                                    % (type(block).__name__)))
                                continue
                        block.write_into(output)

                    return output.getvalue().encode('utf-8')

            def append_fragment(frag_content, frag_index):
                fatal = frag_index == 1 or not skip_unavailable_fragments
                if frag_content:
                    fragment_filename = '%s-Frag%d' % (ctx['tmpfilename'], frag_index)
                    try:
                        file, frag_sanitized = sanitize_open(fragment_filename, 'rb')
                        ctx['fragment_filename_sanitized'] = frag_sanitized
                        file.close()
                        frag_content = pack_fragment(frag_content, frag_index)
                        self._append_fragment(ctx, frag_content)
                        return True
                    except EnvironmentError as ose:
                        if ose.errno != errno.ENOENT:
                            raise
                        # FileNotFoundError
                        if not fatal:
                            self.report_skip_fragment(frag_index)
                            return True
                        else:
                            ctx['dest_stream'].close()
                            self.report_error(
                                'fragment %s not found, unable to continue' % frag_index)
                            return False
                else:
                    if not fatal:
                        self.report_skip_fragment(frag_index)
                        return True
                    else:
                        ctx['dest_stream'].close()
                        self.report_error(
                            'fragment %s not found, unable to continue' % frag_index)
                        return False

            max_workers = self.params.get('concurrent_fragment_downloads', 1)
            if can_threaded_download and max_workers > 1:
                self.report_warning('The download speed shown is only of one thread. This is a known issue')
                _download_fragment = lambda f: (f, download_fragment(f)[1])
                with concurrent.futures.ThreadPoolExecutor(max_workers) as pool:
                    futures = [pool.submit(_download_fragment, fragment) for fragment in fragments]
                    # timeout must be 0 to return instantly
                    done, not_done = concurrent.futures.wait(futures, timeout=0)
                    try:
                        while not_done:
                            # Check every 1 second for KeyboardInterrupt
                            freshly_done, not_done = concurrent.futures.wait(not_done, timeout=1)
                            done |= freshly_done
                    except KeyboardInterrupt:
                        for future in not_done:
                            future.cancel()
                        # timeout must be none to cancel
                        concurrent.futures.wait(not_done, timeout=None)
                        raise KeyboardInterrupt

                for fragment, frag_index in map(lambda x: x.result(), futures):
                    fragment_filename = '%s-Frag%d' % (ctx['tmpfilename'], frag_index)
                    down, frag_sanitized = sanitize_open(fragment_filename, 'rb')
                    fragment['fragment_filename_sanitized'] = frag_sanitized
                    frag_content = down.read()
                    down.close()
                    result = append_fragment(decrypt_fragment(fragment, frag_content), frag_index)
                    if not result:
                        return False
            else:
                for fragment in fragments:
                    frag_content, frag_index = download_fragment(fragment)
                    result = append_fragment(frag_content, frag_index)
                    if not result:
                        return False

            self._finish_frag_download(ctx)
        return True
