;;; puz_04_take2.el --- AOC 2025 Day 4 second try -*- lexical-binding: t; -*-

;; Requires the functions from aoc-functions.el


(puz-load "../data/04_data.dat")
(puz-grid-init)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Version using rectangle logic, rather slow
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Version using search-forward, and puz-grid-get-nab
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Version treating buffer as array
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

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


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Version using the cl-loop magic
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun puz-solve-part1d ()
  "Solve Part 1, count number of rolls (@) with less than 4 rolls around it"
  (with-current-buffer "*puz-scratch*"
    (let ((target ?@))
    (cl-loop for pos from (point-min) below (point-max)
             when (eq (char-after pos) target)
             count (< (puz-grid-count-nab pos target) 4)
             ))))

(message "Solution d for part 1 is = %S" (puz-solve-part1d))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Benchmark versions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(benchmark-run 1 (puz-solve-part1a))
;;(20.631744597 1 0.282676994) (1 RUN)

(benchmark-run 10 (puz-solve-part1b))
;; (5.552760011 1 0.28712363100000005) (10 RUNS)

(benchmark-run 10 (puz-solve-part1c))
;; (5.354362332 1 0.29195927499999996) (10 RUNS)

(benchmark-run 10 (puz-solve-part1d))
;; (5.054557688 0 0.0) (10 RUNS)





