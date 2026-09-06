n;;; puz_02.el --- AOC 2025 Day 02 -*- lexical-binding: t; -*-


;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; Reset all AOC (puz- name-space) and unload aoc-functions
;;(puz-reset)

;; Requires the functions from aoc-functions.el
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file

; load into "*puz-scratch*" buffer
(puz-load "../data/02_data.dat")

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (mapcar (lambda (range) (split-string range "-")) (split-string  (buffer-string) "," t))))

;(puz-parse)  ; eval with C-x C-e to inspect parsed output

(defun puz-solve-part1 (parsed)
  "Solve Part 1. using cl-loop and rx, not a very fast solution"
  (let ((res 0))
    (dolist (pair parsed)
      (cl-incf res (cl-loop
                    for num from (string-to-number (cl-first pair)) to (string-to-number (cl-second pair))
                    when (string-match-p
                          (rx bol (group (one-or-more digit))(backref 1) eol) (number-to-string num))
                    sum num)))
    res))

(message "Solution for part 1 is = %S" (puz-solve-part1 (puz-parse)))

(defun puz-solve-part2 (parsed)
  "Solve Part 2. using cl-loop and rx, not a very fast solution"
  (let ((res 0))
    (dolist (pair parsed)
      (cl-incf res (cl-loop
                    for num from (string-to-number (cl-first pair)) to (string-to-number (cl-second pair))
                    when (string-match-p
                          (rx bol (group (one-or-more digit))(one-or-more (backref 1)) eol) (number-to-string num))
                    sum num)))
    res))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))

;; Improved version (after code review by Claude.ai)

; might be more readable to have as a constant.
(defconst puz-rx-doubled
  (rx bos (group (one-or-more digit))(backref 1) eos)
  "A number digits can be split into exactly two identical groups."
  )

(defconst puz-rx-two-or-more
  (rx bos (group (one-or-more digit))(one-or-more (backref 1)) eos)
  "A number digits can be split into at least two identical groups."
  )

; combine the two solutions and do some cl-loop "magic"
(defun puz-solve-part1-2 (parsed)
  "Solve Part 1 and 2. using cl-loop and rx, not a very fast solution"
  (cl-loop for (low high) in parsed
             for (r1 r2) = (cl-loop for num from (string-to-number low) to (string-to-number high)
                                         for s = (number-to-string num)
                                         when (string-match-p puz-rx-doubled s) sum num into part1
                                         when (string-match-p puz-rx-two-or-more s) sum num into part2
                                         finally return (list part1 part2))
             sum r1 into res1
             sum r2 into res2
             finally return (list res1 res2)))

(message "Solution for part 1 and 2 is = %S" (puz-solve-part1-2 (puz-parse)))
