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
;;(message "%S" (nth 1 (puz-parse)) )

;; Not very nice solution, works, however hard coded number of lines
;; (which is different in test and real data).
(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED data."
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
  "Solve Part 1 using PARSED data."
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
  "Solve Part 1 using PARSED data."
  (let* ((ops (car (last parsed))) ; gap list of operators
         (operands (apply #'cl-mapcar #'list (butlast parsed)))); operand lists
    (cl-reduce #'+ ; avoids calling + with 1000 operands
           (cl-mapcar (lambda (op opr) (apply (intern-soft op) (mapcar #'string-to-number opr)))
                      ops operands)))) ; map over both lists

(message "Solution for part 1 c is = %S" (puz-solve-part1-c  (puz-parse)))


(defun puz-parse2 ()
  "Parse `*puz-scratch*' for part 2."
  (with-current-buffer "*puz-scratch*"
    (let* ((textlines (split-string  (buffer-string) "\n" t)))
      textlines)))
(message "%S" (nth 1 (puz-parse2)) )


;; The magic is in the `(apply #'cl-mapcar #'string operands)' which reads columns into strings
(defun puz-solve-part2-a (parsed)
  "Solve part 2 from PARSED.
Assume no 0 in the input might not be general but applies to mine."
  (let* ((ops (nreverse (split-string (car (last parsed))))) ; gap list of operators
         (operands (mapcar #'nreverse (butlast parsed))); operand lists
         (operandlist (mapcar #'string-to-number (apply #'cl-mapcar #'string operands)))
         (oper nil)
         (res 0))
    (dolist (x operandlist)
      (if (= 0 x)
          (progn
            (cl-incf res (apply (intern-soft (pop ops)) oper))
            (setq oper nil))
        (push x oper)))
    (cl-incf res (apply (intern-soft (pop ops)) oper))
    res))

(puz-solve-part2-a (puz-parse2))


;; refactor and split out the ugly list splitting.

(defun puz-split-list (orglist split)
  "Split ORGLIST at SPLIT into a list of lists."
  (let* ((collect)
         (newlist))
    (dolist (x orglist)
            (if (equal x split)
                (progn (push (nreverse collect) newlist) (setq collect nil))
              (push x collect)))
    (nreverse (push (nreverse collect) newlist))))

;; Splitting out the split-list function, cleans up code, and allows to use cl-loop
(defun puz-solve-part2-b (parsed)
  "Solve part 2 from PARSED.
Assume no 0 in the input might not be general but applies to mine."
  (let* ((ops (nreverse (split-string (car (last parsed))))) ; grap list of operators
         ;; select the rows of operands and reverse
         (operands (mapcar #'reverse (butlast parsed))));
    (cl-loop for x in (puz-split-list
                       (mapcar #'string-to-number (apply #'cl-mapcar #'string operands)) 0 )
             for op in ops
             sum (apply (intern-soft op) x))))

(puz-solve-part2-b (puz-parse2))



;;; puz_06.el ends here

