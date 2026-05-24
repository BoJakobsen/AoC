;;; puz_01.el --- AOC 2025 Day 1 -*- lexical-binding: t; -*-

;; The `-*-' line tells Emacs to read this file under lexical-binding rules.
;; Without it, closures and `let' scoping would behave the old (dynamic) way.


(require 'cl-lib)

(defun puz-load (path)
  "Read PATH into a fresh `*puz-scratch*' buffer."
  ;; `get-buffer-create' returns the buffer if it exists, makes it if not.
  ;; We then `erase-buffer' so re-runs start clean instead of accumulating.
  ;; `with-current-buffer' temporarily makes BUF the "current" buffer so
  ;; that `erase-buffer' and `insert-file-contents' operate on it.
  (let ((buf (get-buffer-create "*puz-scratch*")))
    (with-current-buffer buf
      (erase-buffer)
      (insert-file-contents path))))

;; Top-level call: loads the data when this file is eval'd.
;; Comment this out if you want to load manually instead.
(puz-load "../data/01_data.dat")


(defun puz-parse ()
  "Parse `*puz-scratch*' into a list of (DIR . N) cons pairs.
DIR is the character ?L or ?R; N is the integer rotation amount.
Each line of input must look like \"L68\" or \"R5\"."
  (with-current-buffer "*puz-scratch*"
    ;; `let*' (with the star) lets each binding see the previous ones —
    ;; `lines' needs `text', `pairs' would need `lines'.
    (let* ((text  (buffer-string))                  ; whole buffer as one string
           (lines (split-string text "\n" t))       ; t = drop empty strings
           (pairs (mapcar
                   ;; Per-line parser: first char is direction, rest is number.
                   ;;   (aref line 0)              -> character at index 0
                   ;;   (substring line 1)         -> string from index 1 to end
                   ;;   (string-to-number ...)     -> "68" -> 68
                   ;;   (cons CHAR NUM)            -> (CHAR . NUM) dotted pair
                   (lambda (line)
                     (cons (aref line 0)
                           (string-to-number (substring line 1))))
                   lines)))
      pairs)))

;; (puz-parse)  ; eval with C-x C-e to inspect parsed output

;; dolist version
(defun puz-solve-part1 (pairs)
  "Solve Part 1: count how many times the dial ends a move on position 0.

The dial has 100 positions (0..99), starts at 50.  Each instruction is
a direction and a number; R adds, L subtracts; wrap mod 100.
The puzzle counts every instruction whose ending position is exactly 0."
  (let* ((pos   50)             ; current dial position
         (zeros 0))              ; running count of zero-landings
    (dolist (p pairs)
      ;; Inner let: scoped to this single instruction.
      ;; Picks the math function (+ or -) based on direction.
      ;; #'+ is the *function* + (vs. plain + which would be a variable lookup).
      (let ((dir  (if (= (car p) ?R) #'+ #'-))    ; function to apply
            (turn (cdr p)))                       ; how far to turn
        ;; `funcall' applies a function held in a variable.
        ;; Equivalent to (+ pos turn) or (- pos turn) depending on dir.
        ;; `mod' wraps correctly for negative results in elisp.
        (setq pos (mod (funcall dir pos turn) 100)))
      ;; After the move, check if we landed on 0.
      (when (= pos 0)
        (setq zeros (1+ zeros))))
    zeros))


(message "Solution dolist for part 1 is = %S" (puz-solve-part1  (puz-parse)))

(defun puz-solve-part1-loop (pairs)
  "Solve part 1: using cl-loop"
  (cl-loop with pos = 50
           for p in pairs
           for dir = (if (= (car p) ?R) #'+ #'-)
           for turn = (cdr p)
           do (setq pos (mod (funcall dir pos turn) 100))
           count (= pos 0)))

(message "Solution loop for part 1 is = %S" (puz-solve-part1-loop  (puz-parse)))


(defun puz-solve-part1-reduce (pairs)
  "Solve part 1: using seq-reduce"
  (seq-reduce
   (lambda (state p)
     (let* ((pos (car state))
            (cnt (cdr state))
            (dir (if (= (car p) ?R) #'+ #'-))
            (turn (cdr p))
            (pos (mod (funcall dir pos turn) 100))
            (cnt (if (= pos 0) (+ cnt 1) cnt)))
       (cons pos cnt)))
   pairs
   (cons 50 0)))


(message "Solution reduce for part 1 is = %S" (cdr (puz-solve-part1-reduce  (puz-parse))))


;;; puz_01.el ends here
