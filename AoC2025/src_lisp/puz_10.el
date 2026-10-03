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
           (push (string-to-number (string-replace "."  "0" (string-replace "#" "1" (nreverse val1))) 2) diagrams)
           (push (puz-decode-schematics val2) schematics)
           (push val3 requirements))))
      (list diagrams schematics requirements ))))

(defun puz-decode-schematics (str)
  (let ((str-list (split-string str " " t) ))
    (mapcar  (lambda (str-but)
               (cl-loop for num-str in (split-string (nreverse str-but) "[^0-9]+" t)
                        sum (expt 2 (string-to-number num-str) )))
             str-list)))

;; (puz-parse)


(defun puz-solve-one (diagram schematics)
  (let ((N 0)
         (seen (make-hash-table :test 'eql))
         (leafs (list 0)))
    (puthash 0 t seen)
    (while (not (gethash diagram seen))
      (cl-incf N)
      (setq leafs (cl-loop for leaf in leafs
                           append (cl-loop for schematic in schematics
                                           for new-state = (logxor leaf schematic)
                                           unless (gethash new-state seen)
                                           do (puthash new-state t seen) and collect new-state
                                           ))))
    N))

(defun puz-solve-part1 (parsed)
  "Solve Part 1 using PARSED."
  (let ((diagrams (nth 0 parsed))
        (n-schematics (nth 1 parsed)))
    (cl-loop for dia in diagrams
             for sche in n-schematics
             sum (puz-solve-one dia sche))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;;; puz_10.el ends here
