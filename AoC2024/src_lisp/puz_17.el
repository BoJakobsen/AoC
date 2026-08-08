;;; puz_17.el --- AOC 2024 Day 17 -*- lexical-binding: t; -*-

;;; Commentary:
;; Lisp version of day 17 from 2024.
;; Main goal is to learn pcase and cl-defstruct

;;; Code:

;; Setup AOC solving framework

;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; Reset all AOC (puz- name-space) and unload aoc-functions
;; (puz-reset)

;; Requires the functions from aoc-functions.el
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file
(require 'cl-lib')

;; load into "*puz-scratch*" buffer
(puz-load "../data/17_data.dat")

;; Solution code

;; Define a structure for the cpu state
(cl-defstruct puz-cpu
  "CPU structure, a,b,c registers, pc: program counter, jnx: jump not zero flag, out: out buffer, prog: program."
  a b c (pc 0) (jnz nil) (out nil) prog)

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*' return a `puz-cpu' struct."
  (with-current-buffer "*puz-scratch*"
    (let* ((lines (split-string (buffer-string) "\n" t)))
      (make-puz-cpu
       :a (string-to-number (nth 1 (split-string (nth 0 lines) ": " t)))
       :b (string-to-number (nth 1 (split-string (nth 1 lines) ": " t)))
       :c (string-to-number (nth 1 (split-string (nth 2 lines) ": " t)))
       :prog (mapcar #'string-to-number (split-string (nth 1 (split-string (nth 3 lines) ": " t)) "," t ))))))

;; test parser
;; (puz-parse)

(defun puz-get-op (cpu)
  "Return current op-code from CPU at current pc."
  (nth (puz-cpu-pc cpu) (puz-cpu-prog cpu)))

(defun puz-get-operand (cpu)
  "Return current operand from CPU at current pc."
  (nth (1+ (puz-cpu-pc cpu)) (puz-cpu-prog cpu)))

(defun puz-get-combo-operand (cpu)
  "Return current combo-operand from CPU at current pc."
  (pcase (puz-get-operand cpu)
    (4
     (puz-cpu-a cpu))
    (5
     (puz-cpu-b cpu))
    (6
     (puz-cpu-c cpu))
    (7
     (error "Combo operand 7, is not in use"))
    (operand ; operand 0 -- 3 are passed through
     operand)))

;; Version using bit-vise operations, deduced from the original puzzle.
(defun puz-exec-op (cpu)
  "Execute op-code at current program counter (pc), in-place update CPU state, if jnz fired return `'jnz'."
  (pcase (puz-get-op cpu)
    (0
     (setf (puz-cpu-a cpu)  (ash (puz-cpu-a cpu) (- (puz-get-combo-operand cpu)))))
    (1
     (setf (puz-cpu-b cpu)  (logxor (puz-cpu-b cpu)  (puz-get-operand cpu))))
    (2
     (setf (puz-cpu-b cpu)  (logand (puz-get-combo-operand cpu) 7 )))
    ((and 3 (guard (not (zerop (puz-cpu-a cpu)))))
     (setf (puz-cpu-pc cpu)  (puz-get-operand cpu))
     'jnz)
    (3
     nil) ; jnz not taken falling through to pc + 2
    (4
     (setf (puz-cpu-b cpu)  (logxor (puz-cpu-b cpu)  (puz-cpu-c cpu))))
    (5
     (push (logand (puz-get-combo-operand cpu) 7) (puz-cpu-out cpu)))
    (6
     (setf (puz-cpu-b cpu)  (ash (puz-cpu-a cpu) (- (puz-get-combo-operand cpu)))))
    (7
     (setf (puz-cpu-c cpu)  (ash (puz-cpu-a cpu) (- (puz-get-combo-operand cpu)))))
    (op ; matches all and binds to op
     (error "Bad opcode: %S" op))))

(defun puz-advance-program (cpu)
  "Updates CPU at current pc and advance pc."
    (unless (eq 'jnz (puz-exec-op cpu))
      (cl-incf (puz-cpu-pc cpu) 2)))

(defun puz-solve-part1 ()
  "Solve Part 1: Run program until pc is larger than length of program."
  (let ((cpu (puz-parse)))
    (while (< (puz-cpu-pc cpu) (length (puz-cpu-prog cpu)))
      (puz-advance-program cpu))
    (nreverse (puz-cpu-out cpu))))

(message "Solution for part 1 is = %S" (puz-solve-part1))

;;; puz_17.el ends here
