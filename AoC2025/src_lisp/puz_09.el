;;; puz_09.el --- AOC 2025 Day 09 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 09

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



;; Macro define (puz-load-data) and (puz-load-testdata) with current filenames
(puz-loaders "../data" 09)
;; Load puzzle data into "*puz-scratch*" buffer
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let* ((textlines (split-string  (buffer-string) "\n" t))
           (point-list  (mapcar (lambda (line) (mapcar #'string-to-number (split-string line ","))) textlines)))
      point-list)))
;; (puz-parse)

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (cl-loop for ((a1 b1) . rest) on parsed ; combined "tail loop" and deconstruction
           when rest ; needed as rest might be empty, which breaks inner loop
           maximize (cl-loop
                     for (a2 b2) in rest
                        maximize  (* (1+ (abs (- a1 a2)))(1+ (abs (- b1 b2)))))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))


;; Setup utilities for compressing the grid into a 2d structure
(defvar puz-xs)
(defvar puz-ys)
(defvar puz-grid-width)
(defvar puz-grid-height)
(defvar puz-grid)

(let ((sorted (mapcar #'seq-uniq (mapcar #'sort  (apply #'cl-mapcar #'list (puz-parse))))))
  (setq puz-xs (car sorted))
  (setq puz-ys (cadr sorted))
  (setq puz-grid-width (1+ (* 2 (length puz-xs))))
  (setq puz-grid-height (1+ (* 2 (length puz-ys))))
  )

(defun puz-compress (p)
  (list (1+ (* 2 (seq-position puz-xs (car p)))) (1+ (* 2 (seq-position puz-ys (cadr p))))))

;; Could use some "check for bound"
(defun puz-grid-set (p z)
  (aset puz-grid (+ (car p) (* (cadr p) puz-grid-width)) z))

;; Could use some "check for bound"
(defun puz-grid-get (p)
  (aref puz-grid (+ (car p) (* (cadr p) puz-grid-width))))

(defun puz-grid-print ()
    (cl-loop for n from 0  to (1- puz-grid-height)
             do (message "%s \n " (seq-subseq puz-grid (* n puz-grid-width) (* (1+ n) puz-grid-width)))
             ))

;; Generate compressed grid
(defun puz-generate-compressed-grid (parsed)
  (setq puz-grid (make-vector (* puz-grid-width  puz-grid-height) 0))
  (let* ((pairs (puz-parse))
         (pairs-comp (mapcar #'puz-compress pairs))
         (pairs-comp-wrap (append pairs-comp (list (car pairs-comp))))
         )
    (cl-loop for (p1 . rest) on pairs-comp-wrap
             when rest
             do (progn
                  (cl-loop for x from (min (car p1) (caar rest)) to (max (car p1) (caar rest)) 
                           do (puz-grid-set (list x (cadr p1)) 1 ))
                  (cl-loop for y from (min (cadr p1) (cadar rest)) to (max (cadr p1) (cadar rest))  
                           do (puz-grid-set (list (car p1) y) 1 ))))))

;; now we need to flood fill the outside, assuming no "hidden inner parts not part of the area"
(defun puz-grid-fill ()
 (let ((stack (list 0)))
  (aset puz-grid 0 -1)
  (while stack
    (let ((pos (pop stack)))
      (dolist (offset  (list -1 1 puz-grid-width puz-grid-height))
        (let ((new-pos (+ pos offset)))
          (when (and (<= 0 new-pos) (> (* puz-grid-width puz-grid-height) new-pos)
                   (= 0 (aref puz-grid new-pos)))
            (aset puz-grid new-pos -1)
            (push new-pos stack)
            ))))))
 (cl-loop for p across-ref puz-grid
          when (= p 0) do (setf p 1)
          when (= p -1) do (setf p 0))
 )




(puz-generate-compressed-grid (puz-parse) )
(puz-grid-fill)
(puz-grid-print)



;;; puz_09.el ends here
