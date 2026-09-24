;;; puz_08.el --- AOC 2025 Day 08 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 08

;;; Code:

;; Reset all AOC (puz- name-space) and unload aoc-functions
;;(puz-reset) bound to : C-c p r

;; add the AOC local helper functions
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                               (file-name-directory
                                (or load-file-name buffer-file-name))))
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file

(require 'cl-lib)

;; Macro define (puz-load-data) and (puz-load-testdata) with current filenames
(puz-loaders "../data" 08)
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

(defun puz-sqr-diff (x1 x2)
  "Distance squared between X1 and X,"
  (expt (- x1 x2) 2))

(defun puz-make-pairs (parsed)
  (sort
   (cl-loop for i from 0
           for (p1 . rest) on parsed ; combined "tail loop" and deconstruction
           when rest ; needed as rest might be empty, which breaks inner loop
           append (cl-loop
                   for j from (1+ i)
                   for p2 in rest
                   collect (list (apply #'+ (cl-mapcar #'puz-sqr-diff p1 p2)) i j)))
   :key #'car))

;; the double loop is what takes time, so lets store that for both part 1 and 2
(defvar puz-pairs)
(setq puz-pairs (puz-make-pairs (puz-parse)))

(defun puz-find (dset i)
  "Find root node for node I in DSET recursive.
Do path compression on returning."
  (let ((parent (aref dset i) ))
      (if (= i parent); base case, root is reached
      i
      (aset dset i (puz-find dset parent))))) ; path compress, and return root

(defun puz-union (dset dsize i j ntrees)
  "Combine tree containing node I and J."
  (let ((iroot (puz-find dset i))
        (jroot (puz-find dset j)))
    (if (= iroot jroot)  ; i and j are in same set nothing to do
        ntrees
      (if (>= (aref dsize iroot) (aref dsize jroot)) ; iroot is the bigger one
          (progn
            (aset dset jroot iroot)
            (aset dsize iroot (+ (aref dsize iroot) (aref dsize jroot))))
        (aset dset iroot jroot)
        (aset dsize jroot (+ (aref dsize iroot) (aref dsize jroot))))
      (1- ntrees))))

(defun puz-solve-part1 (parsed pairs p)
  "Solve Part 1 using PARSED and PAIRS."
  (let* ((ntrees (length parsed))
        (parent (vconcat (number-sequence 0 (1- ntrees)  )))
        (treesize (make-vector ntrees 1 )))
    (cl-loop for n from 0 to p
             for (s i j) in pairs
             do (puz-union parent treesize i j ntrees))
    (cl-reduce #'*  (seq-subseq (sort treesize :reverse t) 0 3))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse) puz-pairs 999))

(defun puz-solve-part2 (parsed pairs)
  "Solve Part 2 using PARSED and PAIRS."
  (let* ((ntrees (length parsed))
        (parent (vconcat (number-sequence 0 (1- ntrees)  )))
        (treesize (make-vector ntrees 1 )))
    (cl-loop for n from 0
             for (s i j) in pairs
             until (= 1 (setq ntrees (puz-union parent treesize i j ntrees)))
             finally return (* (car (nth i parsed)) (car (nth j parsed)))))))

(message "Solution for part 2 is = %S" (puz-solve-part2  (puz-parse) puz-pairs))


;;; puz_08.el ends here
