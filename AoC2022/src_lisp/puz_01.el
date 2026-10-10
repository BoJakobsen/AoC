;;; puz_01.el --- AOC 2022 Day 01 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2022 Day 01

;;; Code:

;; Reset all AOC (puz- name-space) and unload aoc-functions
;;(puz-reset)

;; add the AOC local helper functions
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                               (file-name-directory
                                (or load-file-name buffer-file-name))))
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file

(require 'cl-lib)



;; Macro define (puz-load-data) and (puz-load-testdata) with current filenames
(puz-loaders "../data" 01)
;; Load puzzle data into "*puz-scratch*" buffer
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'. Return list of list of strings."
  (with-current-buffer "*puz-scratch*"
    (let ((puz-string (buffer-string))
          (parsed nil))
      (mapcar 'split-string (split-string puz-string "\n\n" t)))))

(puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for elf in parsed
           maximize (cl-loop for item in elf
                             sum (string-to-number item))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;;; puz_01.el ends here
