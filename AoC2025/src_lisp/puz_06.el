;;; puz_06.el --- AOC 2025 Day 06 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 06

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
(puz-load "../data/06_data.dat")

;; For grid problem 
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let* ((textlines (split-string  (buffer-string) "\n" t))
           (lines  (mapcar #'split-string textlines))
           )
      lines)))
(length (nth 3 (puz-parse)))  
(message "%s" (nth 3 (puz-parse)) )

;; Not very nice solution, works, however hard coded number of lines
;; (which is different in test and real data). 
(defun puz-solve-part1 (parsed)
  "Solve Part 1"
  (cl-loop for op in (nth 4 parsed)
           for a1 in (nth 0 parsed)
           for a2 in (nth 1 parsed)
           for a3 in (nth 2 parsed)
           for a4 in (nth 3 parsed)
           do (message "%s" op)   
           sum (funcall (intern-soft op) (string-to-number a1) (string-to-number a2) (string-to-number a3)(string-to-number a4) )))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;; Learned about cl-mapcar and apply, more lisp like and general solution
(defun puz-solve-part1-b (parsed)
  "Solve Part 1"
  (let* ((parsed (nreverse parsed))
         (ops (pop parsed))
         (operands (apply #'cl-mapcar #'list parsed))); transpose to list of list of operands for each
    (apply #'+  ; easy sum list
           (cl-mapcar (lambda (op opr) (apply (intern-soft op) (mapcar #'string-to-number opr)))
                      ops operands)))) ; map over both lists

(message "Solution for part 1 b is = %S" (puz-solve-part1-b  (puz-parse)))


;; Slightly cleaner version after Claude.ai review
;; Avoid manipulating the parsed list with reverse and pop
;; Learned last and butlast, and remembered cl-reduce for the last sum.
(defun puz-solve-part1-c (parsed)
  "Solve Part 1."
  (let* ((ops (car (last parsed))) ; gap list of operators 
         (operands (apply #'cl-mapcar #'list (butlast parsed)))); operand lists
    (cl-reduce #'+ ; avoids calling + with 1000 operands  
           (cl-mapcar (lambda (op opr) (apply (intern-soft op) (mapcar #'string-to-number opr)))
                      ops operands)))) ; map over both lists

(message "Solution for part 1 c is = %S" (puz-solve-part1-c  (puz-parse)))


;;; puz_06.el ends here
