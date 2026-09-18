;;; puz_07.el --- AOC 2025 Day 07 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 07

;; Implicit assumption is that all solutions end up at the bottom
;; nothing "falls of the sites". This is true for my data,
;; maybe also in genereal for this AOC problem.

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
(puz-loaders "../data" 7)
;; Load puzzle data into "*puz-scratch*" buffer
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; Deff special (global) vars here.
(defvar puz-cache)
(defvar puz-grid-n-cols)

; not total standard DFS as we only need total of reachable splitters
(defun puz-count-splits (pos tree)
  "DFS recursive solve of part 1, counts number of splits from POS on TREE."
  (if (or (<= (length tree) pos) (gethash pos puz-cache))
      0  ; Base case, bottom reached or point already visited
    (puthash pos t puz-cache)
    (if (equal (aref tree pos) ?^) ;; Splitter reached
        (1+ (cl-loop for offset in (list -1 1)
                     sum (puz-count-splits (+ pos offset) tree))) ; Split
      (puz-count-splits (+ 1 pos puz-grid-n-cols) tree)))); Move downward

(defun puz-solve-part1 ()
  "Solve Part 1."
  (with-current-buffer "*puz-scratch*"
    (let ((puz-cache (make-hash-table :test 'eql))
          (puz-grid-n-cols (- (line-end-position) (line-beginning-position)))
          (tree (vconcat (buffer-string))))
      (puz-count-splits (seq-position tree ?S) tree))))

(message "Solution for part 1 is = %S" (puz-solve-part1))

(defun puz-count-worlds (pos tree)
  "DFS recursive solve of part 2, counts number of worlds accessible from POS on TREE."
  (if (<= (length tree) pos)
      1  ; Base case, bottom reached per def one world
    (or  (gethash pos puz-cache) ; Short circuit or, if on cache use
         (puthash pos            ; Otherwise calculate and add to cache (also true)
                  (if (equal (aref tree pos) ?^); Splitter reached
                      (cl-loop for offset in (list -1 1)
                                   sum (puz-count-worlds (+ pos offset) tree))
                    (puz-count-worlds (+ 1 pos puz-grid-n-cols) tree)); Progress forward
                  puz-cache))))

(defun puz-solve-part2 ()
  "Solve Part 2."
  (with-current-buffer "*puz-scratch*"
    (let ((puz-cache (make-hash-table :test 'eql))
          (puz-grid-n-cols (- (line-end-position) (line-beginning-position)))
          (tree (vconcat (buffer-string))))
      (puz-count-worlds (seq-position tree ?S) tree))))

(message "Solution for part 2 is = %S" (puz-solve-part2))

;;; puz_07.el ends here
