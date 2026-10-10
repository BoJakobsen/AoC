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

;; (Macro) define (puz-load-data) (C-c p d) and
;;                (puz-load-testdata) (C-c p t)
(puz-loaders "../data" DD)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let ((puz-string (buffer-string))
          (parsed nil))
      nil
         )))

;;(puz-parse)  

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (let (())
    nil
  ))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED."
  (let (())
    nil
    ))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;; (aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)


;;; puz_DD.el ends here
