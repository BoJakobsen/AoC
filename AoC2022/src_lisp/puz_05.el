;;; puz_05.el --- AOC 2022 Day 05 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 05

;;; Code:

;; Reset all AOC (puz- name-space) and unload aoc-functions
;; (puz-reset)

;; add the AOC local helper functions
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                               (file-name-directory
                                (or load-file-name buffer-file-name))))
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file
(require 'cl-lib)

;; (Macro) define (puz-load-data) (C-c p d) and
;;                (puz-load-testdata) (C-c p t)
(puz-loaders "../data" 05)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) 

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; Problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'.
Returns list with starting-stacks drawing, and processed procedures"
  (with-current-buffer "*puz-scratch*"
    (let* ((puz-parts (split-string (buffer-string) "\n\n" t))
           (starting (split-string (car puz-parts) "\n" t))
           (procedures (puz-mapcar2 #'string-to-number
                                    (mapcar (lambda (line) (split-string line (rx (one-or-more (not digit))) t))
                                            (split-string (cadr puz-parts) "\n" t)))))
      (list starting procedures)
      )))

(defun puz-decode-drawing (start-draw)
 (let* ((col ))
  (cl-loop for i from 1
           while (setq col (seq-position (car (last start-draw)) (+ i ?0))) ; find which number exists
           collect (cl-loop for lin from 0 to (- (length start-draw) 2)
                            for box = (string (aref  (nth lin start-draw) col))
                            if (not (string-blank-p box))
                            collect box))))

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (let ((stacks (puz-decode-drawing (car parsed))))
    (message "%s" stacks) 
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


;;; puz_05.el ends here
