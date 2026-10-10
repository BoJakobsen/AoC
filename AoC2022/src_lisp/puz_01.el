;;; puz_01.el --- AOC 2022 Day 01 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 01

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

;; (Macro) define (puz-load-data) (C-c p d) and
;;                (puz-load-testdata) (C-c p t)
(puz-loaders "../data" 1)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'. Return list (of elf's ) of list (of calories)."
  (with-current-buffer "*puz-scratch*"
    (puz-mapcar2 #'string-to-number (mapcar #'split-string (split-string (buffer-string) "\n\n" t)))))

(puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED.
Sum of calories for the elf having maximal total calories."
  (cl-loop for elf in parsed
           maximize (cl-loop for item in elf
                             sum item)))

(message "Solution for part 1 is = %S" (puz-solve-part1 (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED.
Sum of calories for the 3 elves carrying largest total amount of calories."
  (let ((elves 3)
        (total-cal (sort (mapcar (lambda (l) (apply #'+ l)) parsed) :reverse t)))
    (apply #'+ (seq-subseq total-cal 0 elves))))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;;(aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)

;;; puz_01.el ends here
