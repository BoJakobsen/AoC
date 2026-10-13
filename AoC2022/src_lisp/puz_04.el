;;; puz_04.el --- AOC 2022 Day 04 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 04

;;; Code:

;; Reset all AOC (puz- name-space) and unload aoc-functions
;; (puz-reset)

;; add the AOC local helper functions
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                               (file-name-directory
                                (or load-file-name buffer-file-name))))
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file
(require 'cl-lib)

;; (Macro) define (puz-load-data) (C-c p d) and
;;                (puz-load-testdata) (C-c p t)
(puz-loaders "../data" 04)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; Problem specific parser
;; Can likely be simplified with a regexp.
(defun puz-parse ()
  "Parse `*puz-scratch*'.
List of list of pairs (also lists)."
  (with-current-buffer "*puz-scratch*"
      (puz-mapcar2 (lambda (range) (mapcar #'string-to-number (split-string range "-")))  (mapcar (lambda (pair) (split-string pair ",") )  (split-string (buffer-string) "\n" t)))))

;; (puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED.
Counts pairs where one is fully contained in the other."
  (cl-loop for pair in parsed
           for (a b) =  (sort pair :key #'car) ; presort after start of interval
           for b-in-a = (and (<= (car b) (cadr a)) (<= (cadr b) (cadr a)))
           for a-in-b = (and (= (car a) (car b)) (>= (cadr b) (cadr a)))
           count (or a-in-b b-in-a)))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;; (aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED.
Count pairs with any overlap, presort makes this very simple."
    (cl-loop for pair in parsed
           for (a b) =  (sort pair :key #'car) ; presort after start
           count  (<= (car b) (cadr a)))) ; now just test start of b before (or equal) end of a

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;; (aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)

;;; puz_04.el ends here
