;;; puz_10.el --- AOC 2025 Day 10 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 10

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
(puz-loaders "../data" 10)
;; Load puzzle data into "*puz-scratch*" buffer
(puz-load-data) ; bound to : C-c p d
;;(puz-load-testdata) ; bound to : C-c p t

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let ((diagrams nil)
          (schematics nil)
          (requirements nil))
      (dolist (line (split-string (buffer-string) "\n" t ))
        (pcase line
          ((rx bol "[" (let val1 (one-or-more (any ".#"))) "] "
               (let val2 (one-or-more (seq "(" (one-or-more (any "," digit)) ")" (zero-or-more space))))
               "{" (let val3 (one-or-more (any "," digit))) "}" eol)
           (message "%s" val3)
           (push val1 diagrams)
           (push val2 schematics)
           (push val3 requirements))))
      (list diagrams schematics requirements ))))

(puz-parse)

(let ((test nil))
  (push "test" test)
  test
  )

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
)

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;;; puz_10.el ends here
