;;; puz_09.el --- AOC 2025 Day 09 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 09

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
(puz-loaders "../data" 09)
;; Load puzzle data into "*puz-scratch*" buffer
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let* ((textlines (split-string  (buffer-string) "\n" t))
           (point-list  (mapcar (lambda (line) (mapcar #'string-to-number (split-string line ","))) textlines)))
      point-list)))
;; (puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for ((a1 b1) . rest) on parsed ; combined "tail loop" and deconstruction
           when rest ; needed as rest might be empty, which breaks inner loop
           maximize (cl-loop
                     for (a2 b2) in rest
                        maximize  (* (1+ (abs (- a1 a2)))(1+ (abs (- b1 b2)))))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;;; puz_09.el ends here
