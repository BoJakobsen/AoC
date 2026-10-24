;;; puz_07.el --- AOC 2022 Day 07 -*- lexical-binding: t; -*-

;;; Commentary:
;; Advent of Code puzzle 2022 Day 07

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
(puz-loaders "../data" 07)

;; loads current data into *puz-scratch* buffer.
(puz-load-data) ; 

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; Problem specific parser, trivial but kept to keep the structure of the solutions.
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (split-string (buffer-string) "\n"  t)))

;(puz-parse)

(defun puz-get-dir (fulltree path)
  "Find the cons cell of FULLTREE corresponding to PATH (a list of sub dirs).
PATH is assumed to be in revers order, for easy `push' `pop' action on the path"
  (cl-reduce
   (lambda (subtree subdir)
     (assoc subdir subtree))
             (reverse path)  :initial-value fulltree))

;; In hindsight the outer most list could have been "skipped" but this is nice and
;; works with alist methods, even as the final solution manually handles the structure.
(defun puz-parse-tree (parsed)
  "Parse the output of investigate the file structure in PARSED.
Returns a tree structure of alist type.
Assumes that we only traverse each folder ones"
  (let ((cur-dir (list "/"))
        (tree (list (cons "/" nil))))
    (dolist (line parsed)
      (pcase line
        ((rx bol "$ cd /" eol)
         (setq cur-dir (list "/"))); change to top dir
        ((rx bol "$ ls" eol)
         nil ); list current dir (do nothing)
        ((rx bol "$ cd .." eol)
         (pop cur-dir)); navigate to previous dir
        ((rx bol "$ cd " (let dir-name (+ any)) eol)
         (push dir-name cur-dir)); navigate "down" to dir-name
        ((rx bol "dir " (let dir-name (+ any))  eol); listing of a sub dir in current dir
         (push (cons dir-name nil) (cdr (puz-get-dir tree cur-dir)))) ; assume we havn't seen it before
        ((rx bol (let size (+ digit)) " " (let file-name (+ any))  eol); file: size name
         (push (cons file-name (string-to-number size)) (cdr (puz-get-dir tree cur-dir))))  ; assume we havn't seen it before
        (_
         (message "unknown cmd : %S" line))))
    tree))

;; (puz-parse-tree (puz-parse))

;; The Simpel "debug version", loops tree
;; (defun puz-sum-files-simpel (cur-leaf)
;;   (message "Call fkt")
;;   (message "leaf: %s  cdr: %s  type: %s " cur-leaf (cdr cur-leaf) (type-of (cdr cur-leaf)))
;;   (if (numberp (cdr cur-leaf)) ;base case
;;       (progn
;;         (cdr cur-leaf))
;;     (let ((dir-total (cl-loop for branch in (cdr cur-leaf)
;;              sum (puz-sum-files branch))))
;;       dir-total)))

;; test puz-sum-files-simpel
;;(let ((c (cons "/" (list (cons "a" 12 ) (cons "b" (list (cons "dd" 10) (cons "dd" 20 ) ))))))
;;  (puz-sum-files c))

;; Version accumulating dir sizes on the fly, let over lambda style
;; into a local "global" variable (closure).
(defun puz-sum-files (tree)
  "Find size of all directories in TREE.
Returns a list of the directory sizes."
  (let ((dir-sizes nil))
    (cl-labels ((walk (leaf)
      (if (numberp (cdr leaf)) ;base case
        (cdr leaf)
        (let ((dir-total (cl-loop for branch in (cdr leaf)
                                  sum (walk branch))))
          (push dir-total dir-sizes)
          dir-total)))) ; return value for `walk'
      (walk tree)) ; do the recursive walk
    dir-sizes)) ; return the list of dir sizes

;; test puz-sum-files
;;(let ((c (cons "/" (list (cons "a" 12 ) (cons "b" (list (cons "dd" 10) (cons "dd" 20 ) ))))))
;;  (puz-sum-files c))

(defun puz-solve-part1 (parsed max-size)
  "Solve Part 1 using PARSED.
Sum dir sizes larger than MAX-SIZE."
  (let ((tree (puz-parse-tree parsed)))
    (cl-loop for size in (puz-sum-files (nth 0 tree))
             when (< size max-size)
             sum size)))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))
;;(aoc-submit-answer (puz-solve-part1 (puz-parse)) 1)

(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED.
Retun size of smallest dir that needs to be deleted to have the needed space."
  (let* ((tree (puz-parse-tree parsed))
         (total-space  70000000)
         (needed-space 30000000)
         (dir-sizes (puz-sum-files (nth 0 tree)))
         (current-free (- total-space (seq-max dir-sizes)))
         (need-to-delete (- needed-space current-free)))
    (seq-min (seq-keep (lambda (size) (and (> size need-to-delete) size))  dir-sizes ))))

(message "Solution for part 2 is = %S" (puz-solve-part2 (puz-parse)))
;;(aoc-submit-answer (puz-solve-part2 (puz-parse)) 2)

;;; puz_07.el ends here
