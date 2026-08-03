;;; puz_04.el --- AOC 2025 Day 4 different versions -*- lexical-binding: t; -*-

;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; (puz-reset) ; if wished.

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

;; Uses faster count and does not use search-forward
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
(puz-load "../data/04_data.dat"); Reload dataset which was modified

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


;; Part 2, Local optimizations

(defun puz-grid-vec-count-nab2 (pos vgrid target1 target2)
  "Counts number of TARGET1 and TARGET2 charters among the neighbors to POS in vector VGRID representation of grid."
  (let ((acc 0))
      (dolist (offset puz-grid-offsets)
        (when (and (<= 0 (+ pos offset)) (< (+ pos offset) (length vgrid))
                   (or (eq target1 (aref vgrid (+ pos offset))) (eq target2 (aref vgrid (+ pos offset)))))
          (cl-incf acc)))
      acc))

;In-place modify vgrid, and keep track of places where a roll is removed
(defun puz-remove-rolls-vec2 (vgrid)
  "In place removes rolls (@) with less than 4 rolls around it from VGRID (vec rep of grid problem)."
    (let ((pos 0)
          (n-points (length vgrid))
          (n-removed 0)
          (pos-removed ()))
      (while (< pos n-points)
        (when (eq (aref vgrid pos) ?@)
          (when (< (puz-grid-vec-count-nab2 pos vgrid ?@ ?X) 4)
            (aset vgrid pos ?X)
            (push pos pos-removed)
            (cl-incf n-removed)))
        (cl-incf pos))
      (dolist (pos pos-removed)
        (aset vgrid pos ?.))
      n-removed))

(defun puz-solve-part2c ()
  "Solve part 2."
  (let* ((grid (with-current-buffer "*puz-scratch*" (vconcat (buffer-string))))
         (n-removed (puz-remove-rolls-vec2 grid))            
         (acc n-removed))
    (while (< 0 n-removed)
      (setq n-removed (puz-remove-rolls-vec2 grid))
      (setq acc (+ acc n-removed)))
    acc))

(message "Solution c for part 2 is = %S" (puz-solve-part2c))

;; Benchmark the different versions

(puz-load "../data/04_data.dat")

(benchmark-run 1 (puz-solve-part1a))
(21.668299949999998 1 0.34129878800000313);(1 RUN), not byte-compiled 
; (21.396602823 1 0.35108329199999844); (1 RUN), ALL byte-compiled 

(benchmark-run 10 (puz-solve-part1b))
;; (5.552760011 1 0.28712363100000005) (10 RUNS) not byte-compiled
;; (1.243407023 0 0.0) ; (10 RUN), ALL byte-compiled

(benchmark-run 10 (puz-solve-part1c))
;; (5.354362332 1 0.29195927499999996) (10 RUNS) not byte-compiled
;; (0.548879078 0 0.0); (10 RUN), ALL byte-compiled

(benchmark-run 10 (puz-solve-part1d))
;; (5.054557688 0 0.0) (10 RUNS) not byte-compiled
;; (0.5480555829999999 0 0.0) ; (10 RUN), ALL byte-compiled

(benchmark-run 10 (puz-solve-part1e))
;; (7.2881949409999995 0 0.0) (10 RUNS) not byte-compiled
;; (0.7104646609999999 0 0.0) ; (10 RUN), ALL byte-compiled

(benchmark-run 1 (puz-solve-part2a))
;;(17.199423175 2 0.6481852000000003) (1 RUN) not byte-compiled
;; (2.571083029 1 0.338989153); ; (1 RUN), ALL byte-compiled
(puz-load "../data/04_data.dat") ; reload

(benchmark-run 1 (puz-solve-part2b))
;; (24.474821057 2 0.647141916999999) (1 RUN) not byte-compiled
;; (2.4504965679999997 0 0.0); (1 RUN), ALL byte-compiled

(benchmark-run 1 (puz-solve-part2c))
;; (26.320036399 3 1.025400536999996); 1 RUNS, all optimized, not byte-compiled
;; (2.2123564190000002 0 0.0) ; (1 RUN), ALL byte-compiled


;; Profile part 2 
;; (progn 
;;   (profiler-start 'cpu)
;;   (dotimes (_ 5)
;;           (puz-solve-part2c))
;;   (profiler-stop)
;;   (profiler-report))

;; Profile from  solve-part2c, NOT byte-compiled
;; Notice how all functions break down to primitives

      ;; 128990  97% - command-execute
      ;; 128990  97%  - funcall-interactively
      ;; 128990  97%   - eval-defun
      ;; 128990  97%    - apply
      ;; 128990  97%     - edebug--eval-defun
      ;; 128990  97%      - #<native-comp-function eval-defun>
      ;; 128990  97%       - #<native-comp-function F616e6f6e796d6f75732d6c616d626461_anonymous_lambda_38>
      ;; 128990  97%        - elisp--eval-defun
      ;; 128990  97%         - setq
      ;; 128990  97%          - let
      ;; 128990  97%           - progn
      ;; 128990  97%            - progn
      ;; 128989  97%             - let
      ;; 128989  97%              - while
      ;; 128989  97%               - let
      ;; 128989  97%                - puz-solve-part2c
      ;; 128989  97%                 - let*
      ;; 126363  95%                  - while
      ;; 126360  95%                   - setq
      ;; 126358  95%                    - puz-remove-rolls-vec2
      ;; 126358  95%                     - let
      ;; 126252  95%                      - while
      ;; 116947  88%                       - if
      ;; 109526  82%                        - progn
      ;; 109188  82%                         - if
      ;; 108704  81%                          - <
      ;; 108142  81%                           - puz-grid-vec-count-nab2
      ;; 105352  79%                            - let
      ;; 103400  77%                             - let
      ;; 101467  76%                              - while
      ;;  98764  74%                               - let
      ;;  71720  54%                                - if
      ;;  60207  45%                                 - and
      ;;  28078  21%                                  - or
      ;;  25050  18%                                   - eq
      ;;  17303  13%                                    - aref
      ;;   8953   6%                                       +
      ;;  15818  11%                                  - <
      ;;   6567   4%                                     +
      ;;   4669   3%                                     length
      ;;  11234   8%                                  - <=
      ;;   7051   5%                                     +
      ;;   7492   5%                                 - progn
      ;;   5718   4%                                  - setq
      ;;   3042   2%                                     1+
      ;;   7012   5%                                - setq
      ;;   3503   2%                                   cdr
      ;;   3203   2%                                  car
      ;;     91   0%                          + progn
      ;;   5758   4%                        - eq
      ;;   3405   2%                           aref
      ;;   4488   3%                       - setq
      ;;   2272   1%                          1+
      ;;   2788   2%                         <
      ;;    104   0%                      + let
      ;;      1   0%                     <
      ;;   2625   1%                  + puz-remove-rolls-vec2
      ;;      1   0%                  + save-current-buffer
      ;;      1   0%             + profiler-start
      ;;   3811   2%   Automatic GC
      ;;      0   0%   ...



;; Profile from  solve-part2c, ALL byte-compiled
;; It is now clear where the program spends its time

       ;; 10842 100% - command-execute
       ;; 10842 100%  - funcall-interactively
       ;; 10842 100%   - eval-defun
       ;; 10842 100%    - apply
       ;; 10842 100%     - edebug--eval-defun
       ;; 10842 100%      - #<native-comp-function eval-defun>
       ;; 10842 100%       - #<native-comp-function F616e6f6e796d6f75732d6c616d626461_anonymous_lambda_38>
       ;; 10842 100%        - elisp--eval-defun
       ;; 10842 100%         - setq
       ;; 10842 100%          - let
       ;; 10842 100%           - progn
       ;; 10842 100%            - progn
       ;; 10841  99%             - let
       ;; 10841  99%              - while
       ;; 10840  99%               - let
       ;; 10840  99%                - puz-solve-part2c
       ;; 10838  99%                 - puz-remove-rolls-vec2
       ;;  8794  81%                    puz-grid-vec-count-nab2
       ;;     1   0%                   vconcat
       ;;     1   0%                 setq
       ;;     1   0%             + profiler-start
       ;;     0   0%   ...
