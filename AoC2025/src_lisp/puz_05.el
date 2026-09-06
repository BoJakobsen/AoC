;;; puz_05.el --- AOC 2025 Day 05 -*- lexical-binding: t; -*-


;;; Commentary:
;; Advent of Code puzzel 2025 Day 05

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
(puz-load "../data/05_data.dat")

;; For grid problem
; (puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; For problem specific parser
(defun puz-parse ()
  "Parse `*puz-scratch*'."
  (with-current-buffer "*puz-scratch*"
    (let* ((parts (split-string  (buffer-string) "\n\n" t))); split the two kinds of input
      (list (mapcar (lambda (pair) (mapcar #'string-to-number (split-string pair "-" t))) (split-string (nth 0 parts) "\n" t))
            (mapcar #'string-to-number  (split-string (nth 1 parts) "\n" t))))))

;;(puz-parse)

;; Solution using seq-some and loop count
(defun puz-solve-part1 (parsed)
  "Solve Part 1."
  (let ((freshranges (car parsed))
        (avail (cadr parsed)))
    (cl-loop for ingredient in avail
             count (seq-some (lambda (range)
                               (and (<= (car range) ingredient) (>= (cadr range) ingredient)))
                             freshranges))))

(message "Solution for part 1 is = %S" (puz-solve-part1  (puz-parse)))

;; Merging ranges, and calculating length of merged ranges
;; a1 <= b2 and b1 <= a2 is the correct test for overlap
;; if we sort first it simplifies
(defun puz-solve-part2 (parsed)
  "Solve Part 2 using PARSED data."
  (let* ((freshranges (sort (car parsed) :key #'car)) ; sorted ranges on the first element
         (veryfirst (list (pop freshranges)))) 
    (seq-reduce
     (lambda (res next) (+ res (1+ (- (cadr next) (car next))))) 
     (seq-reduce
      (lambda (mearged next)
        (let* ((last (pop mearged)))
          (if (and (<= (car last) (cadr next)) (<= (car next) (cadr last)))
              (push (list (min (car last) (car next)) (max (cadr last) (cadr next))) mearged)
            (push last mearged)
            (push next mearged))
          mearged))
      freshranges veryfirst) 0)))

(message "Solution for part 2 is = %s" (puz-solve-part2  (puz-parse)))


;;; puz_05.el ends here
