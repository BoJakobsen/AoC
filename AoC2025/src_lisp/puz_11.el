;;; puz_11.el --- AOC 2025 Day 11 -*- lexical-binding: t; -*-

;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; Reset all AOC (puz- name-space) and unload aoc-functions
;;(puz-reset)

;; Requires the functions from aoc-functions.el
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file

; load into "*puz-scratch*" buffer
(puz-load "../data/11_data.dat")

;; 
(defun puz-parse ()
  "Parse `*puz-scratch*', return hash tabel of [device]:(outputs)."
  (with-current-buffer "*puz-scratch*"
    (let* ((text (buffer-string))
           (lines (split-string text "\n" t))
           (parsed (make-hash-table :test 'equal)))      
      (dolist (line lines)
              (puthash (substring line 0 3) (split-string (substring line 4 nil) " " t) parsed))
      parsed)))

(setq puz-dat (puz-parse))  ; Store parsed input as global pre-computed var

(defun puz-solve-part1 (node res)
  "Find number of paths using DSF search from NODE to out"
  (if (equal node "out")
      (setq res 1)
    (setq res 0)  
    (if node
        (dolist (next (gethash node puz-dat))
          (setq res (+ res (puz-solve-part1 next res)))))) 
  res)

(message "Solution for part 1 is = %S" (puz-solve-part1 "you" 0))

;; For part 2 search space is MUCH bigger, hence we need caching
(setq puz-cache (make-hash-table :test 'equal))

(defun puz-dfs-count (state target)
  "Find number of paths using DSF search from STATE to TARGET, utilizes puz-cache"
  (let ((res))
    (if (setq res (gethash (list state target) puz-cache))
        ()
      (if (equal state target)
          (setq res 1)
        (setq res 0)  
        (if state
            (dolist (next (gethash state puz-dat))
              (setq res (+ res (puz-dfs-count next target))))))) 
    (puthash (list state target) res puz-cache)
    res))

;; Test improved solver on part 1
(message "Solution for part 1 is = %S" (puz-dfs-count "you" "out"))

;; Utilizing that total number of solutions can be found as:
;; svr -> dac -> fft -> out + svr -> fft -> dac -> out 
;; so no modifications to DFS algorithm is needed.

(message "Solution for part 2 is = %S"
         (+
          (* (puz-dfs-count "svr" "dac") (puz-dfs-count "dac" "fft") (puz-dfs-count "fft" "out"))
          (* (puz-dfs-count "svr" "fft") (puz-dfs-count "fft" "dac") (puz-dfs-count "dac" "out"))))


;; Some benchmarking

(defun puz-solve2 ()
  (setq puz-cache (make-hash-table :test 'equal)) ; clear cache each time
  (+
   (* (puz-dfs-count "svr" "dac") (puz-dfs-count "dac" "fft") (puz-dfs-count "fft" "out"))
   (* (puz-dfs-count "svr" "fft") (puz-dfs-count "fft" "dac") (puz-dfs-count "dac" "out")))
  )

(benchmark-run 100 (puz-solve2))
;; (5.914490324 2 0.5785631069999999) NOTHING compiled
;; (1.405519415 0 0.0)
;; Compiling gave approx a factor 5, but caching is essential
