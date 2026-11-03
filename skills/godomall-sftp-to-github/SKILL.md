---
name: godomall-sftp-to-github
description: Migrate Godomall board attachments and linked downloads from SFTP to GitHub, update article links, verify preservation, and remove superseded files within the authorized scope.
---

# Godomall SFTP to GitHub

Move downloadable files while preserving article titles, text, formatting, images, and unrelated links. Another AI can follow this skill with an authenticated browser, SFTP, Git, and GitHub CLI. The helper script needs only standard Python.

## Scope and preparation

Record the board ID, visible post numbers and internal `sno` IDs, destination repository, backup directory, and user authorization for publication, article edits, and source deletion. Visible numbers are not database IDs. Existing authorization covers the same task; this skill does not grant permission or expand it.

Use the requested browser. For Orca / 고래, load the installed `orca-cli` skill and its version-matched browser reference, then discover and pin the existing `browserPageId`. Keep passwords, cookies, tokens, keys, and administrative HTML out of the public repository and skill. Obtain credentials from the current session or credential manager.

Read [references/godomall-notes.md](references/godomall-notes.md) for observed form behavior, relative URLs, and attachment storage.

1. Read each authorized article and edit form without saving. Back up its original HTML, title, IDs, attachment filenames, and downloadable body links locally outside the Git checkout.
2. Resolve relative links against the public board URL. Percent-decode SFTP paths and preserve Unicode filenames. Leave unrelated product links, decorative images, video embeds, and external tutorials alone. When the downloadable materials include linked wiring diagrams or other images in the source materials directory, inventory their `src` uses too, including diagrams shared by multiple posts.
3. Back up every exact SFTP file. Record its remote path, local backup, size, SHA-256, and referring articles. Map opaque attachment filenames by comparing bytes against the board download, not by size or basename alone. Inspect archive member names without running installers.
4. Inventory shared-file dependencies before deletion. Search other relevant boards/pages for source URLs. Retain files with unresolved references outside the migration scope and report them; do not edit those other articles without authorization. Defer shared files until all authorized referring articles have migrated.

## Process one article at a time

1. Put unmodified original files in stable article-specific repository directories. Add a concise README with the source article, filename, size, and SHA-256. Keep backups and private administrative/configuration files out of commits. For files too large for ordinary Git storage, use assets on a release in the same repository and link them from the article README. Keep original bytes intact; use stable asset names and preserve original filenames as release display labels and manifest metadata. Check an existing asset before retrying an upload instead of overwriting it blindly.
2. Commit and push with the intended GitHub account. Download each file through its final public URL and compare its complete SHA-256 to the backup. A push or HTTP 200 alone is insufficient. Run `scripts/verify_artifact.py SOURCE --url URL` for this check.
3. Re-read the live article to detect concurrent edits. Replace only inventoried download `href` values and matching material-image `src` values, preserving link text, dimensions, styling, and surrounding HTML. A moved image must not leave an embedded `src` pointing at a deleted SFTP file. Percent-encode GitHub URL paths for Unicode, spaces, and special characters.
4. Save through the authenticated form. Verify the persisted body and public page. Remove obsolete attachment registrations only after their files have been published and verified, so the page does not display dead old downloads.
5. Before source deletion, recheck the live SFTP hash against the backup and confirm no remaining known references depend on it. Remove exactly the eligible path and verify absence. Never recursively remove board/product directories. An application may leave the physical file after deleting its attachment record. Identical legacy copies require their own mapping and reference check.
6. Save a completion record before proceeding to the next visible number: destination commit/URLs, verified hashes, public-page checks, removed attachment records, deleted paths, retained shared paths, and backup paths. On mismatches, authentication loss, unknown references, or failed saves, stop the affected article before further deletion. Check persisted state before retrying any ambiguous write.

## Resume and finish

Resume from records instead of blindly repeating mutations. Inspect the destination files, saved article, attachment registrations, and SFTP paths to locate the unfinished step. A missing source requires a verified backup and published copy before completion.

After the last article, verify all public links and eligible deletions, update the repository index, and report completed posts, file counts, and retained sources or exceptions. Link the repository's skill directory so another AI can read `SKILL.md` or install that folder in its skill directory.
