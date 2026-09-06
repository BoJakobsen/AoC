;;; puz_03.el --- AOC 2025 Day 03 -*- lexical-binding: t; -*-

;;; Commentary:


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

;; Load puzzle data into "*puz-scratch*" buffer
(puz-load "../data/03_data.dat")

;; A slightly sub-optimal parser, seq-map is properly better
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (mapcar (lambda (string) (vconcat (mapcar #'string-to-number (split-string string "" t)))) (split-string (buffer-string) "\n" t))))

(defun puz-vec-to-num (vec)
  "Return number constructed from the digits in VEC (Horner's method)."
  (seq-reduce (lambda (a b)  (+ (* 10 a) b)) vec 0))

(defun puz-find-largest (v)
  "Return (maxval pos) for V."
  (let ((maxval (seq-max v)))
    (list maxval (seq-position v maxval))))

;; loop based function
(defun puz-solve (parsed ndig)
  "General solver on PARSED for NDIG digits."
  (cl-loop for line in parsed
           sum (puz-vec-to-num
                (cl-loop with pos = 0
                         for n from (- ndig 1) downto 0
                         for (maxval maxpos) = (puz-find-largest (seq-subseq line pos (- (length line) n)))
                         do (setq pos (+ pos (1+ maxpos)))
                         collect maxval))))

(message "Solution for part 1 is = %S" (puz-solve  (puz-parse) 2))
(message "Solution for part 2 is = %S" (puz-solve  (puz-parse) 12))

;; recursive version, maybe more pure lisp like
(defun puz-construct-largest (line n start)
  "General recursive solver, return N numbers from LINE starting at START."
  (unless (= n 0) ; implicitly returns a nil as base case, hence cons works.
    (let* ((slice (seq-subseq line start (- (length line) (1- n))))
           (maxval (seq-max slice))
           (maxpos (seq-position slice maxval)))
      (cons maxval (puz-construct-largest line (1- n) (+ start (1+ maxpos)))))))

(defun puz-solve-recursive (parsed ndig)
  (cl-loop for line in parsed
           sum (puz-vec-to-num
                (puz-construct-largest  line ndig 0)
                )))

(message "Recursive Solution for part 1 is = %S" (puz-solve-recursive  (puz-parse) 2))
(message "Recursive Solution for part 2 is = %S" (puz-solve-recursive  (puz-parse) 12))

;;; puz_03.el ends here
