;;; aoc-functions.el --- Advent of Code functions (boj@boj.dk)  -*- lexical-binding: t; -*-

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Requirements
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;; Commentary:
;; 

(require 'cl-lib)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Loader functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Code:

(defun puz-load (path)
  "Read PATH into a fresh *puz-scratch* buffer."
  (let ((buf (get-buffer-create "*puz-scratch*")))
    (with-current-buffer buf
      (erase-buffer)
      (insert-file-contents path)
      (whitespace-mode) ;; show space and newline
      (setq truncate-lines t)))) ;; do not wrap

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; For grid based puzzles
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar puz-grid-n-cols nil "Width of the current puzzle grid (chars)." )
(defvar puz-grid-n-rows nil "Height of the current puzzle grid (lines)." )
(defvar puz-grid-offsets nil "Precomputed 8-neighbor buffer offsets." )

(defun puz-grid-init ()
  "Measures the grid size in *puz-scratch* and pre-computes 8-neighbor offsets."
  (with-current-buffer "*puz-scratch*"
    (goto-char (point-min))
    (setq puz-grid-n-cols (- (line-end-position) (line-beginning-position)))
    (setq puz-grid-n-rows (count-lines (point-min) (point-max)))
    (let ((stride (1+ puz-grid-n-cols)))
      (setq puz-grid-offsets
            (list (- -1 stride) (- stride) (- 1 stride)
                  (- 1)                     (+ 1)
                  (+ stride -1) (+ stride)   (+ stride 1 )))))
  (message "Grid size. n-cols: %d, n-rows: %d" puz-grid-n-cols puz-grid-n-rows))

(defun puz-grid-get-nab (pos)
  "Return the 8 nabours at the point POS, in the current buffer."
    (let ((chars))
      (dolist (offset puz-grid-offsets)
        (push (char-after (+ pos offset))  chars))
      (nreverse chars)))

;; Does not generate an list of the chars
(defun puz-grid-count-nab (pos &rest target)
  "Counts number of TARGET charters among the neighbors to POS."
    (let ((acc 0))
      (dolist (offset puz-grid-offsets)
        (when (memq (char-after (+ pos offset))  target)
          (cl-incf acc)))
      acc))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; General tools
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun puz-reset ()
  "Unbind every symbol whose name start with \"puz-\".
Wipes both variable values and function definitions."
  (interactive)
  (unload-feature 'aoc-functions t)
  (let ((count 0))
    (mapatoms
     (lambda (sym)
       (when (string-prefix-p "puz-" (symbol-name sym))
         (when (boundp sym)  (makunbound sym)  (cl-incf count))
         (when (fboundp sym) (fmakunbound sym) (cl-incf count)))))
    (message "Unbound %d puz- bindings" count)))


(provide 'aoc-functions)
;;; aoc-functions.el ends here
