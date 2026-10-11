;;; puz_02.el --- AOC 2022 Day 02 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 02


;; Numerical encoding

;; Rock = 0, paper = 1, scissor = 2

;;  (<- 0 <- 1 <- 2 )
;;  A - B mod 3
;;  0 - 1 = -1 = 2  (A loos)
;;  0 - 2 = -2 = 1  (A win)
;;  1 - 2 = -1 = 2  (A loos)
;;  1 - 0 = 1       (A win)
;;  2 - 0 = 2       (A Loos)
;;  2 - 1 =         (A win) 

;; Therefore logic is:
;; (A - B mod 3 = res)
;; 0 Tie
;; 1 A win
;; 2 A Loos

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
(puz-loaders "../data" 02)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; Problem specific parser
;; works but now very pity
;; (defun puz-parse ()
;;   "Parse `*puz-scratch*'."
;;   (with-current-buffer "*puz-scratch*"
;;     (let* ((dat (string-replace "A" "0" (buffer-string)))
;;            (dat (string-replace "B" "1" dat))
;;            (dat (string-replace "C" "2" dat))
;;            (dat (string-replace "X" "0" dat))
;;            (dat (string-replace "Y" "1" dat))
;;            (dat (string-replace "Z" "2" dat)))
;;       (puz-mapcar2 #'string-to-number (mapcar #'split-string (split-string dat "\n" t))))))


;; Problem specific parser
;; Simplified after AI code-review.
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let* ((dat (split-string (buffer-string) "\n" t)))
      (mapcar (lambda (line) (list (- (aref line 0) ?A) (- (aref line 2) ?X  )) ) dat)
      )))

;;(puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for (A B) in parsed
           for res = (mod (- B A) 3)
           if (= res 0) ; draw
           sum (+ (1+ B) 3)
           if (= res 1) ;; you win
           sum (+ (1+ B) 6)
           if (= res 2) ;; you loos
           sum (1+ B)))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

;; Cleaner, inspired by AI code-review
(defun puz-solve-part1b (parsed)
  "Solve Part 1 using PARSED."
  (let ((score  [3 6 0]))
   (cl-loop for (them me) in parsed
           for res = (mod (- me them) 3)
           sum (+ (1+ me) (aref score res))
           )))

(message "Solution for part 1 (b) is = %S" (puz-solve-part1b  (puz-parse)))


(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED."
  (let (())
    nil
    ))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;; (aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)


;;; puz_02.el ends here
