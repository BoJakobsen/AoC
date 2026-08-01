;;; puz_04.el --- AOC 2025 Day 4 different versions -*- lexical-binding: t; -*-

;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; Requires the functions from aoc-functions.el
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file

(puz-load "../data/04_data.dat"); Load data into *puz-scratch* buffer
(puz-grid-init); sets puz-grid-n-cols, puz-grid-n-rows, puz-grid-offsets (8- nab)

;; Part 1. Version using rectangle logic, rather slow

;; based on snippet from web
(defun puz-count-in-rectangle (char)
  "Count number of CHAR in the active rectangle region."
  (if (region-active-p)
      (let* ((beg (region-beginning))
             (end (region-end))
             (rect-text (mapconcat 'identity (extract-rectangle beg end) "")))
        (cl-count char rect-text))
    (message "No active region")))

(defun puz-count-square (char)
  "Count number of CHAR in 3x3 grid around current point
handles boundaries"
  (save-mark-and-excursion
  (let ((col (current-column))
        (row (line-number-at-pos)))
    (when (< 1 row ) (goto-line (1- row)))
    (when (< 0 col ) (move-to-column (1- col)))
    (set-mark (point))    
    (if (< row  (line-number-at-pos (1- (point-max))))
        (goto-line (1+ row))
      (goto-line row))
    (move-to-column (+ 2 col)) ;; needs to be 2 to put point outside region
    (rectangle-mark-mode 1))
  (puz-count-in-rectangle char)))

(defun puz-solve-part1a ()
  "Solve Part 1, count number of rolls (@) with less than 4 rolls around it"
  (with-current-buffer "*puz-scratch*"
    (goto-char (point-min))
    (let ((Nacc 0)
          (Nroll 0))
      (while (search-forward "@" nil t)
        (forward-char -1)
        (setq Nroll (1- (puz-count-square ?@)))
        (when (> 4 Nroll)
          (setq Nacc (1+ Nacc)))
        (forward-char 1))
      Nacc)))

(message "Solution a for part 1 is = %S" (puz-solve-part1a))


;;; Part 1. Version using search-forward, and puz-grid-get-nab

;; Version using search and get-nab function
(defun puz-solve-part1b ()
  "Solve Part 1, count number of rolls (@) with less than 4 rolls around it"
  (with-current-buffer "*puz-scratch*"
    (goto-char (point-min))
    (let ((acc 0))
      (while (search-forward "@" nil t)
        (when (< (cl-count ?@ (puz-grid-get-nab (1- (point)))) 4 )
          (setq acc (1+ acc))))
      acc)))

(message "Solution b for part 1 is = %S" (puz-solve-part1b))


;;; Part 1. Version treating buffer as array

;; uses faster count and does not use search-forward
(defun puz-solve-part1c ()
  "Solve Part 1, count number of rolls (@) with less than 4 rolls around it"
  (with-current-buffer "*puz-scratch*"
    (let ((pos (point-min))
          (acc 0)
          (target ?@)
          )
      (while (< pos (point-max))
        (when (eq (char-after pos) target)
          (when (< (puz-grid-count-nab pos target) 4)
            (cl-incf acc)))
        (cl-incf pos))
      acc)))

(message "Solution c for part 1 is = %S" (puz-solve-part1c))



;;; Part 1. Version using the cl-loop magic

(defun puz-solve-part1d ()
  "Solve Part 1, count number of rolls (@) with less than 4 rolls around it"
  (with-current-buffer "*puz-scratch*"
    (let ((target ?@))
    (cl-loop for pos from (point-min) below (point-max)
             when (eq (char-after pos) target)
             count (< (puz-grid-count-nab pos target) 4)
             ))))

(message "Solution d for part 1 is = %S" (puz-solve-part1d))



;;; For Part 2. Version that in-place modifies the buffer

(defun puz-replace-after (pos char)
  "Replaces the character after POS with CHAR in current buffer."
  (goto-char pos)
  (delete-char 1)
  (insert-char char))

(defun puz-remove-rolls ()
  "Remove rolls (@) with less than 4 rolls around it. Return number of removed rolls."
  (with-current-buffer "*puz-scratch*"
    (let ((pos (point-min))
          (acc 0))
      (while (< pos (point-max))
        (when (eq (char-after pos) ?@)
          (when (< (puz-grid-count-nab pos ?@ ?X) 4)
            (puz-replace-after pos ?X)
            (cl-incf acc)))
        (cl-incf pos))
      (goto-char (point-min))
      (subst-char-in-region (point-min) (point-max) ?X ?. t)
      acc)))


(defun puz-solve-part2a ()
  "Solve part 2. Modifies the '*puz-scratch* buffer."
    (with-current-buffer "*puz-scratch*"
      (let ((buffer-undo-list t) ;disable undo tracking for speed
            (acc 0))
        (while (< 0 (setq removed (puz-remove-rolls)))
          (setq acc (+ acc removed)))
        acc)))

(message "Solution a for part 2 is = %S" (puz-solve-part2a))
(puz-load "../data/04_data.dat"); Reload dataset

;;; Treat buffer as vector, part one and two.

(defun puz-grid-vec-count-nab (pos vgrid &rest targets)
  "Counts number of TARGET charters among the neighbors to POS in vector VGRID representation of grid."
  (let ((acc 0)
        (n-points (length vgrid)))
      (dolist (offset puz-grid-offsets)
        (when (and (<= 0 (+ pos offset)) (< (+ pos offset) n-points)
                   (memq (aref vgrid (+ pos offset))  targets))
          (cl-incf acc)))
      acc))

;; For test solve part 1 ones more for control of vector mechanism
(defun puz-solve-part1e ()
  "Solve part 1 (again)."
    (with-current-buffer "*puz-scratch*"
      (let* ((grid (vconcat (buffer-string))) ; full buffer as an array
            (acc 0)
            (pos 0)
            (n-points (length grid)))
        (while (< pos n-points)
          (when (eq (aref grid pos) ?@)
            (when (< (puz-grid-vec-count-nab pos grid ?@) 4)
              (cl-incf acc)))
          (cl-incf pos))
        acc)))

(puz-load "../data/04_data.dat")
(message "Solution e for part 1 is = %S" (puz-solve-part1e))

(defun puz-remove-rolls-vec (vgrid)
  "Remove rolls (@) with less than 4 rolls around it from VGRID (vec rep of grid prblem)."
    (let ((pos 0)
          (n-points (length vgrid))
          (n-removed 0))
      (while (< pos n-points)
        (when (eq (aref vgrid pos) ?@)
          (when (< (puz-grid-vec-count-nab pos vgrid ?@ ?X) 4)
            (aset vgrid pos ?X)
            (cl-incf n-removed)))
        (cl-incf pos))
      (setq pos 0)
      (while (< pos n-points)
        (when (eq (aref vgrid pos) ?X) (aset vgrid pos ?.))
        (cl-incf pos))
      (cons n-removed vgrid)))

(defun puz-solve-part2b ()
  "Solve part 2."
    (with-current-buffer "*puz-scratch*"
      (let* ((grid (vconcat (buffer-string)))
            (reslist (puz-remove-rolls-vec grid))
            (grid (cdr reslist))
            (n-removed (car reslist))
            (acc n-removed))
        (while (< 0 n-removed)
          (setq reslist (puz-remove-rolls-vec grid))
          (setq grid (cdr reslist))
          (setq n-removed (car reslist))
          (setq acc (+ acc n-removed)))
        acc)))

(puz-load "../data/04_data.dat")
(message "Solution b for part 2 is = %S" (puz-solve-part2b))


;; Benchmark versions

(benchmark-run 1 (puz-solve-part1a))
;;(20.631744597 1 0.282676994) (1 RUN)

(benchmark-run 10 (puz-solve-part1b))
;; (5.552760011 1 0.28712363100000005) (10 RUNS)

(benchmark-run 10 (puz-solve-part1c))
;; (5.354362332 1 0.29195927499999996) (10 RUNS)

(benchmark-run 10 (puz-solve-part1d))
;; (5.054557688 0 0.0) (10 RUNS)

(benchmark-run 10 (puz-solve-part1e))
;;  (10 RUNS)

(benchmark-run 1 (puz-solve-part2a))
;;(17.199423175 2 0.6481852000000003) (1 RUN)
(puz-load "../data/04_data.dat") ; reload

(benchmark-run 1 (puz-solve-part2b))
;; (24.474821057 2 0.647141916999999) (1 RUN)
;; (26.361648776 2 0.6519366610000006)


