# Observed Godomall behavior (2026-11-03)

These are site observations, not universal API guarantees. Inspect the current form before using endpoints or fields.

- Public article: `/board/view.php?bdId=traningdatab&sno=57`. Admin view/edit: `/board/article_view.php` and `/board/article_write.php?bdId=traningdatab&sno=57&mode=modify`.
- The board ID is spelled `traningdatab`. Visible post 1 was `sno=57`; IDs are not consecutive.
- The edit POST form was `#frmWrite`, with `bdId`, `sno`, `mode=modify`, `contents`, and other existing fields. Inspect its action and preserve fields instead of inventing a write API.
- Froala can create a wrapper with the same ID as the original textarea. Read `textarea[name=contents]`, not the first `#article-write-editor`. When editing live, update the current Froala instance too, so submission does not overwrite the textarea with stale editor content.
- Existing attachment names appeared in `const uploadFileNm = [...]`. The UI inserted hidden `delFile[index]` checkboxes. A parser of server-rendered HTML must explicitly add those checked deletion fields when removing attachments.
- Removing an attachment record left physical SFTP copies behind. Verify remote deletion separately.
- Opaque attachments existed under both `/data/board/upload/traningdatab/` and the distinct case-sensitive legacy `/data/board/upload/TraningDataB/`. Never infer safe deletion from size alone.
- Body links like `../data/goods/swgoods/4028/TIDCS_DSP2833x.zip` resolve against the public board URL to `/data/goods/swgoods/4028/TIDCS_DSP2833x.zip`. Common libraries and examples may also be referenced by other boards.
- Some HTTP downloads included extra data after a valid ZIP. The original SFTP ZIP matched the response's exact prefix. Store the original SFTP bytes, not the larger response; do not strip data without a verified source match. `verify_artifact.py --allow-trailing-response` diagnoses this prefix case. GitHub checks must use the default exact comparison.
- Saves can return JavaScript for a processing iframe rather than JSON. Verify the persisted editor and public article instead of relying on a response shape.
- Saving some legacy articles automatically rewrote local image `src` values to Godomall CDN URLs. Verify image counts and hashes before accepting this server-generated change; do not interpret it as an intentional image migration or delete the old images yourself.
- Re-reading an edit form can normalize HTML serialization without changing the parsed DOM. If the raw concurrency check differs, compare parsed markup, text, attributes, and links before treating it as an edit. Do not replace actual concurrent content changes merely because the text appears similar.
- Admin body search used `searchField=contents`, a board-specific `bdId`, and broad `rangDate[]` dates. Omitting `bdId` did not search all boards. Enumerate boards, check pagination, and inspect returned articles for exact paths.
- The SFTP service required legacy `ssh-rsa` negotiation. Retain known-host checks and the user's host settings. Paramiko 5 removed legacy `ssh-rsa`; Paramiko 3.5 worked with password authentication. Do not weaken host verification or change global SSH settings.

No credentials belong here. Discover the current tab, connection parameters, credentials, and directories in each session.
