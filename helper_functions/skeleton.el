;;; puz_DD.el --- AOC YYYY Day DD -*- lexical-binding: t; -*-

;; Uses functions from aoc-functions.el 

;; If needed clean up from earlier work
;;(puz-reset)

; load into "*puz-scratch*" buffer
(puz-load "../data/DD_data.dat")

;;; For puzzle specific parses
;; (defun puz-parse ()
;;   "Parse `*puz-scratch*' "
;;   (with-current-buffer "*puz-scratch*"
;;     ))
;; (puz-parse)  

;;; For grid problems
;; (puz-grid-init)

(defun puz-solve-part1 (parsed)
  "Solve Part 1"
  (with-current-buffer "*puz-scratch*"
    
    ))

(message "Solution for part 1 is = %d" (puz-solve-part1  (puz-parse)))
