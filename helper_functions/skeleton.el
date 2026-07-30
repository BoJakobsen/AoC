;;; puz_DD.el --- AOC YYYY Day DD -*- lexical-binding: t; -*-


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
(puz-load "../data/DD_data.dat")

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let ((parsed nil))
      ( 
         )
      parsed)))

;;(puz-parse)  ; eval with C-x C-e to inspect parsed output

;; For grid problem 
; (puz-grid-init)  ; sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

(defun puz-solve-part1 (parsed)
  "Solve Part 1"
  (with-current-buffer "*puz-scratch*"
    (let ((res nil))
      (
       )
      res)))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
