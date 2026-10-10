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

;; Macro define (puz-load-data) and (puz-load-testdata)
;; loads current data into *puz-scratch* buffer.
(puz-loaders "../data" 01)
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'. Return list of list of strings."
  (with-current-buffer "*puz-scratch*"
    (let ((puz-string (buffer-string))
          (parsed nil))
      (puz-mapcar2 'string-to-number (mapcar 'split-string (split-string puz-string "\n\n" t))))))

;;(puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for elf in parsed
           maximize (cl-loop for item in elf
                             sum item)))

(message "Solution for part 1 is = %S" (puz-solve-part1 (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED."
  (let ((total-cal (reverse (sort (mapcar (lambda (l) (apply #'+ l)) parsed)))))
    (apply #'+ (seq-subseq total-cal 0 3 ))))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
(aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)

;;; puz_01.el ends here
