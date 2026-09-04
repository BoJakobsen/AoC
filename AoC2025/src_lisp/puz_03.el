;;; puz_03.el --- AOC 2025 Day 03 -*- lexical-binding: t; -*-

;;; Commentary:


;;; Code:

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
(puz-load "../data/03_data.dat")

;; A slightly not optimized parser, seq-map is properly better
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (mapcar (lambda (string) (vconcat (mapcar #'string-to-number (split-string string "" t)))) (split-string (buffer-string) "\n" t))))

;(puz-parse)

(defun find-largest (v)
  "Return (maxval pos) for V."
    (list (setq maxval (seq-max v)) (seq-position v maxval)))

(defun vec-to-num (vec)
  "Return number from digits VEC."
  (seq-reduce (lambda (a b)  (+ (* 10 a) b)) vec 0))

(defun puz-solve (parsed N)
  "General solver on PARSED for N digits."
  (cl-loop for line in (puz-parse)
           sum (vec-to-num
                (cl-loop with pos = 0
                         for n from (- N 1) downto 0
                         for (maxval maxpos) = (find-largest (seq-subseq line pos (- (length line) n)))
                         do (setq pos (+ pos (1+ maxpos)))
                         collect maxval))))

(message "Solution for part 1 is = %S" (puz-solve  (puz-parse) 2))
(message "Solution for part 2 is = %S" (puz-solve  (puz-parse) 12))

;;; puz_03.el ends here
