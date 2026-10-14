;;; puz_06.el --- AOC 2022 Day 06 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 06

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
(puz-loaders "../data" 06)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; Almost not needed, but keeps the structure
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (buffer-string)))

;; (puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for ch across parsed
           for i from 1
           for buf = (append (last buf 3 )  (list ch))
           until (= 4 (length (seq-uniq buf)))
           finally return i))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;; (aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

;; Very compact solution (can give both part 1 (n=4) and 2 (n=14))
(defun puz-solve-part2 (parsed n)
  "Solve using PARSED, for N unique chars."
  (cl-loop for i from n
           thereis (and (= n (length (seq-uniq (substring parsed (- i n) i)))) i)))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse) 14))
(message "Solution for part 1 is = %S" (puz-solve-part2 (puz-parse) 4))
;;(aoc-submit-answer (puz-solve-part2 (puz-parse) 14) 2)


;;; puz_06.el ends here
