;;; puz_03.el --- AOC 2022 Day 03 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 03

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
(puz-loaders "../data" 03)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'.
Almost not necessary just list of the lines"
  (with-current-buffer "*puz-scratch*"
    (let ((puz-string (buffer-string)))
      (split-string puz-string))))

;; (puz-parse)

(defun puz-score (item)
  "Score function. a - z : 1 - 26, A -Z : 27 - 52." 
  (if (<= ?a item)
      (+ (- item ?a) 1)
    (+ (- item ?A) 27)))

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED.
Each rucksack is split in half and items in both parts scored."
  (cl-loop for rucksack in parsed
           for n-items = (/ (length rucksack) 2)
           sum (puz-score (car (seq-uniq (apply #'seq-intersection (seq-split rucksack n-items)))))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED."
  (let (())
    nil
    ))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;; (aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)


;;; puz_03.el ends here
