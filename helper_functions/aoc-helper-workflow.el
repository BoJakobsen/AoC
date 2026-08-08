;;; aoc-helper-workflow.el --- Advent of Code workflow helper  -*- lexical-binding: t; -*-

;; Copyright (C) 2023  Arthur Miller
;; Copyright (C) 2026  Bo Jakobsen

;; Original author: Arthur Miller <arthur.miller@live.com>
;; Modified by:     Bo Jakobsen <boj@boj.dk>
;; Keywords: advent-of-code, convenience, tools

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <https://www.gnu.org/licenses/>.

;;; AI Disclosure:
;; The modifications and additions relative to Arthur Miller's
;; original (the workflow around a browser-free setup, the description
;; fetching and Org conversion, the example-block extraction, and the
;; surrounding refactoring) were developed with the assistance of
;; Anthropic's Claude, primarily via Claude Code using the Opus 4.8
;; model. All AI-suggested changes were reviewed by the modifier, who
;; takes responsibility for the derived work. The AI was primarily
;; applied to the added portions rather than Arthur's upstream code.
;; No warranty is provided as to correctness or fitness for purpose of
;; any code in this file — reviewed or not. See the GNU General Public
;; License above for the full terms.

;;; Commentary:

;; A heavily modified version of Arthur Miller's Advent of Code skeleton
;; generator, reworked for my personal AoC workflow: Emacs Lisp solutions on
;; a machine without a web browser.  The in-Emacs input download builds on an
;; idea by Matthias Paulmier <https://github.com/mattplm>; see the Reddit
;; thread for the original discussion:
;; https://www.reddit.com/r/emacs/comments/187h4e3/aoc_puzzle_skeleton_generator/kbivv4t/

;; To install, put this file somewhere in your `load-path' and require it.

;; For each day the helper can:
;;   - open (or create) the solution file, seeding a new file from a skeleton
;;     template with the YYYY and DD placeholders substituted;
;;   - download the personal puzzle input; and
;;   - fetch the puzzle description as an Org file -- via pandoc, or a
;;     libxml/`shr' fallback -- so it can be read without a browser.

;; Layout: files live under aoc-repo/AoC<year>/, split into a source
;; sub-directory (`aoc-src-dir', default "src_lisp") and a data sub-directory
;; (`aoc-data-dir', default "data").  File names come from the `aoc-src-file',
;; `aoc-input-file' and `aoc-desc-file' format strings (puz_NN.el, NN_data.dat,
;; puz_NN.org).  Change `aoc-repo' to relocate everything, or the sub-directory
;; / format vars to match a different layout.  Set `aoc-year' to the challenge
;; year, or nil for the current year.

;; Commands:
;;   aoc-do-day          Open/create a day: code + input + description.
;;   aoc-get-description  (Re)fetch just the description; it overwrites, so run
;;                        it after solving part 1 to pull in part 2.
;;   aoc-grab-example     In a description buffer, with point in an example
;;                        block, save that block to the day's NN_testdata.dat.

;; Session cookie (needed for the personal input and for part 2):
;;   1. Log in to adventofcode.com in a browser.
;;   2. Open the developer tools (F12) -> Storage/Application -> Cookies.
;;   3. Copy the value of the single "session" cookie (128 hex chars).
;;   4. Save just that value into the file named by `aoc-cookie' (default
;;      "session.txt" next to this file).  Surrounding quotes/whitespace are
;;      tolerated.  AoC session cookies expire after a few weeks.
;; Part-1 descriptions are public, so they are fetched even without a cookie.

;;; Code:
(require 'url)        ; declares url-request-extra-headers as a special var
(require 'subr-x)     ; string-trim
(require 'shr)        ; libxml render, fallback when pandoc is absent

(defvar aoc-repo (expand-file-name "~/Projekter/AoC")
  "Root directory holding the per-year AoC<year> directories.")
(defvar aoc-year "2025"
  "Challenge year as a string.  Set to nil to use the current year.")
(defvar aoc-src-dir "src_lisp"
  "Sub-directory under AoC<year> holding the Lisp solution files.")
(defvar aoc-data-dir "data"
  "Sub-directory under AoC<year> holding the input/test data files.")
(defvar aoc-src-file "puz_%02d.el"
  "`format' string, taking the day number, for a solution file name.")
(defvar aoc-input-file "%02d_data.dat"
  "`format' string, taking the day number, for a puzzle input file name.")
(defvar aoc-test-file "%02d_testdata.dat"
  "`format' string, taking the day number, for an example/test data file.")
(defvar aoc-desc-file "puz_desc_%02d.org"
  "`format' string, taking the day number, for the puzzle description file.")
(defvar aoc-cookie (expand-file-name "session.txt" default-directory)
  "File holding the adventofcode.com session cookie value.")
(defvar aoc-skeleton (expand-file-name "skeleton.el" default-directory)
  "Template file whose contents seed a new day's code buffer, when it exists.")

(defun aoc--session-headers ()
  "Return `url-request-extra-headers' carrying the AoC session cookie.
Returns just a User-Agent header when no cookie file exists, so public
part-1 descriptions can still be fetched."
  (let ((agent (cons "User-Agent"
                     "https://github.com/BoJakobsen by e_claude@f77.dk")))
    (if (file-exists-p aoc-cookie)
        (let ((cookie (with-temp-buffer
                        (insert-file-contents aoc-cookie)
                        (string-trim (buffer-string) "[ \t\n\r\"]+" "[ \t\n\r\"]+"))))
          (list (cons "Cookie" (concat "session=" cookie)) agent))
      (list agent))))

(defun aoc-download-input (year day dest)
  "Download the puzzle input for YEAR and DAY into file DEST.
Does nothing if DEST already exists.  Requires a valid session cookie
in `aoc-cookie'."
  (let ((url (format "https://adventofcode.com/%s/day/%s/input" year day))
        (url-request-extra-headers (aoc--session-headers)))
    (unless (file-exists-p dest)
      (make-directory (file-name-directory dest) t)
      (url-copy-file url dest))))

(defun aoc--extract-articles (html)
  "Return the concatenated <article class=\"day-desc\"> blocks from HTML.
AoC wraps each puzzle part in one such article (part 2 appears once
unlocked); everything else on the page is navigation we skip.  A solved
part is immediately followed by a \"<p>Your puzzle answer was ...</p>\"
sibling, which we keep and attach to that part -- handy when redoing a
puzzle and checking against the known answer."
  (let ((pos 0) (parts nil) (open "<article class=\"day-desc\">") (close "</article>"))
    (while (string-match (regexp-quote open) html pos)
      (let* ((start (match-beginning 0))
             (end (string-match (regexp-quote close) html (match-end 0))))
        (if (not end)
            (setq pos (length html))          ; malformed; stop scanning
          (setq end (+ end (length close)))
          (let ((block (substring html start end))
                ;; A short window past </article>; the answer <p> is tiny.
                (after (substring html end (min (length html) (+ end 300)))))
            ;; Pull in the "Your puzzle answer was N." paragraph, if present.
            (if (string-match
                 "\\`[ \t\r\n]*\\(<p>Your puzzle answer was\\(?:.\\|\n\\)*?</p>\\)"
                 after)
                (setq block (concat block "\n" (match-string 1 after))
                      pos (+ end (match-end 0)))
              (setq pos end))
            (push block parts)))))
    (mapconcat #'identity (nreverse parts) "\n\n")))

(defun aoc--articles-to-org (html)
  "Convert article HTML to Org text, via pandoc when available.
Falls back to a plain-text render through libxml/`shr' otherwise."
  (if (executable-find "pandoc")
      (with-temp-buffer
        (insert html)
        (let ((coding-system-for-read 'utf-8)
              (coding-system-for-write 'utf-8))
          ;; -auto_identifiers keeps pandoc from adding :CUSTOM_ID: drawers.
          (call-process-region (point-min) (point-max) "pandoc"
                               t t nil "-f" "html-auto_identifiers"
                               "-t" "org" "--wrap=none"))
        (buffer-string))
    (with-temp-buffer
      (insert html)
      (let ((dom (libxml-parse-html-region (point-min) (point-max))))
        (erase-buffer)
        (shr-insert-document dom))
      (buffer-substring-no-properties (point-min) (point-max)))))

(defun aoc-fetch-description (year day dest)
  "Fetch the YEAR/DAY puzzle description and write it as Org to DEST.
DEST is overwritten, so re-running after solving part 1 picks up part 2.
Uses the session cookie when present; part 1 is public without it."
  (let* ((url (format "https://adventofcode.com/%s/day/%s" year day))
         (url-request-extra-headers (aoc--session-headers))
         (tmp (make-temp-file "aoc-desc" nil ".html")))
    (unwind-protect
        (progn
          (url-copy-file url tmp t)
          (let ((articles (aoc--extract-articles
                           (with-temp-buffer
                             (insert-file-contents tmp)
                             (buffer-string)))))
            (make-directory (file-name-directory dest) t)
            (with-temp-file dest
              (insert (format "#+title: Advent of Code %s — Day %s\n" year day))
              (insert (format "[[%s][puzzle page]]\n\n" url))
              (if (string-empty-p articles)
                  (insert "* Description unavailable\n\n"
                          "Not logged in, or the day is not released yet.\n")
                (insert (aoc--articles-to-org articles))))))
      (delete-file tmp))))

;;;###autoload
(defun aoc-get-description (day)
  "(Re)fetch the puzzle description for DAY of `aoc-year' and open it.
Unlike `aoc-do-day', this always overwrites the Org file, so run it
after solving part 1 to pull in part 2."
  (interactive (list (read-number "Which day: ")))
  (unless (< 0 day 26) (error "Invalid day; must be in range [1,25]."))
  (let* ((year (or aoc-year (format-time-string "%Y")))
         (srcdir (expand-file-name
                  aoc-src-dir
                  (expand-file-name (format "AoC%s" year) aoc-repo)))
         (desc (expand-file-name (format aoc-desc-file day) srcdir)))
    (aoc-fetch-description year day desc)
    (find-file desc)
    (revert-buffer t t)          ; show the freshly written file if reopened
    (message "Fetched description for %s day %s" year day)))

(defun aoc--example-at-point ()
  "Return the text inside the Org #+begin_.../#+end_ block around point.
Returns nil when point is not inside such a block."
  (save-excursion
    (let ((case-fold-search t) (orig (line-beginning-position)) beg)
      (end-of-line)
      (when (re-search-backward "^[ \t]*#\\+begin_[a-z]+" nil t)
        (setq beg (line-beginning-position 2))       ; content starts next line
        (when (re-search-forward "^[ \t]*#\\+end_[a-z]+" nil t)
          (let ((end (line-beginning-position)))     ; the #+end_ line
            ;; Only inside the block if its terminator is at/after point.
            (when (>= end orig)
              (buffer-substring-no-properties beg end))))))))

;;;###autoload
(defun aoc-grab-example ()
  "Grab the Org example block at point into the day's test-data file.
Run this in a puzzle description buffer (see `aoc-fetch-description')
with point inside an #+begin_example block.  The block contents are
written to <data>/NN_testdata.dat, with NN and the data directory
derived from the file being visited."
  (interactive)
  (let* ((orgfile (or (buffer-file-name)
                      (user-error "Buffer is not visiting a file")))
         (base (file-name-nondirectory orgfile))
         (day (if (string-match "\\([0-9]+\\)" base)
                  (string-to-number (match-string 1 base))
                (user-error "Cannot determine the day from %s" base)))
         ;; org lives in <year>/<src>/; its grandparent is the year directory.
         (yeardir (file-name-directory
                   (directory-file-name (file-name-directory orgfile))))
         (datadir (expand-file-name aoc-data-dir yeardir))
         (dest (expand-file-name (format aoc-test-file day) datadir))
         (content (or (aoc--example-at-point)
                      (user-error "Point is not inside an Org example block"))))
    (when (string-empty-p content)
      (user-error "The example block at point is empty"))
    (when (or (not (file-exists-p dest))
              (y-or-n-p (format "Overwrite %s? " (file-name-nondirectory dest))))
      (make-directory datadir t)
      (with-temp-file dest (insert content))
      (message "Wrote %d-line example to %s"
               (length (split-string (string-trim-right content) "\n"))
                dest))))

;;;###autoload
(defun aoc-do-day ()
  "Interactively ask and open the code and input file for a given day.

Opens AOC<year>/<day>.el.  When that file does not yet exist and a
skeleton template exists (see `aoc-skeleton'), its contents seed the
new buffer; the buffer is left unsaved so you can save it yourself.
If a session cookie exists (see the comment section at the top of this
file) and there is no input file for the day, the input is downloaded.
The puzzle description is fetched to an Org file next to the code and
shown in a side window."
  (interactive)
  (let* ((year (or aoc-year (format-time-string "%Y")))
         (day (read-number "Which day: "))
         (yeardir (expand-file-name (format "AoC%s" year) aoc-repo))
         (srcdir (expand-file-name aoc-src-dir yeardir))
         (datadir (expand-file-name aoc-data-dir yeardir))
         (lisp (expand-file-name (format aoc-src-file day) srcdir))
         (input (expand-file-name (format aoc-input-file day) datadir))
         (desc (expand-file-name (format aoc-desc-file day) srcdir))
         (new (not (file-exists-p lisp))))
    (unless (< 0 day 26) (error "Invalid day; must be in range [1,25]."))
    (unless (file-exists-p srcdir) (make-directory srcdir t))
    (unless (file-exists-p datadir) (make-directory datadir t))
    (delete-other-windows)
    (dired srcdir)
    (find-file lisp)
    (when (and new (file-exists-p aoc-skeleton))
      (insert-file-contents aoc-skeleton)
      ;; Fill template placeholders with the concrete year and day.
      (let ((case-fold-search nil))
        (dolist (sub `(("YYYY" . ,year)
                       ("DD" . ,(format "%02d" day))))
          (goto-char (point-min))
          (while (search-forward (car sub) nil t)
            (replace-match (cdr sub) t t)))))
    (when (file-exists-p aoc-cookie)
      (aoc-download-input year day input))
    ;; Grab the puzzle text once; re-fetch later (delete DESC) to pull part 2.
    (unless (file-exists-p desc)
      (condition-case err
          (aoc-fetch-description year day desc)
        (error "Could not fetch description: %s"
                        (error-message-string err))))
    ;; Show the description in a side window (fall back to the raw input).
    (cond ((file-exists-p desc)
           (find-file-other-window desc)
           (other-window 1))
          ((file-exists-p input)
           (find-file-other-window input)
           (other-window 1)))))


(provide 'aoc-helper-workflow)
;;; aoc-helper-workflow.el ends here
