;;; puz_DD.el --- AOC YYYY Day DD -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel YYYY Day DD

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
(puz-load "../data/DD_data.dat")

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let ((parsed nil))
      ( 
         )
      parsed)))

;;(puz-parse)  

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
)

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;;; puz_DD.el ends here
