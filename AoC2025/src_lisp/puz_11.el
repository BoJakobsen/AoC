;;; puz_11.el --- AOC 2025 Day 11 -*- lexical-binding: t; -*-

;;; Commentary:

;; Solving AOC puzzle 11 (2025) in elisp (already solved in python).
;;
;; Assumption is that the we have a directed graph without loops (a directed acyclic graph (DAG))
;; This is not explicitly stated in the puzzle, but seems to be the case, at least for the
;; test data and my data-set.

;;; Code:

;; add the AOC local helper function dir to the path
(add-to-list 'load-path
             (expand-file-name "../../helper_functions"
                  (file-name-directory
                   (or load-file-name buffer-file-name))))

;; Reset all AOC (puz- name-space) and unload aoc-functions
;; (puz-reset)

;; Requires the functions from aoc-functions.el
(require 'aoc-functions) ; REMEMBER this does not reload changes from the file
(require 'cl-lib)

; load the data into "*puz-scratch*" buffer
(puz-load "../data/11_data.dat")

;; Not the most general parseer, contains "magic numbers" which is not best practices
;; but ok for AOC
(defun puz-parse ()
  "Parse `*puz-scratch*', return hash tabel of [device]:(outputs)."
  (with-current-buffer "*puz-scratch*"
    (let* ((text (buffer-string))
           (lines (split-string text "\n" t))
           (parsed (make-hash-table :test 'equal)))
      (dolist (line lines)
              (puthash (substring line 0 3) (split-string (substring line 4 nil) " " t) parsed))
      parsed)))

;; ; Store parsed input as global pre-computed variable
(defvar puz-dat)
(setq puz-dat (puz-parse))

;; Initial solution to part 1, no-caching and always ending on out
;; This is keeps as the "naive first try".
;; The solver for part 2 includes part 1

(defun puz-solve-part1 (node)
  "Find number of paths using DFS search from NODE to out."
  (let (res)
    (if (equal node "out")
        (setq res 1)
      (setq res 0)
      (if node
          (dolist (next (gethash node puz-dat))
            (setq res (+ res (puz-solve-part1 next))))))
    res))

(message "Solution for part 1 is = %S" (puz-solve-part1 "you"))

;; For part 2 search space is MUCH bigger, hence we need caching

;; Initial versions use a global cache, ok for AOC but needs care if e.g. dataset canges
(defvar puz-cache)


(setq puz-cache (make-hash-table :test 'equal));; New and clean cache

;; A very Python like solver, works but is not really lisp like
(defun puz-dfs-count1 (state target)
  "Find number of paths using DFS search from STATE to TARGET, utilizes `puz-cache'."
  (let ((res))
    (unless (setq res (gethash (list state target) puz-cache))
      (if (equal state target)
          (setq res 1)
        (setq res 0)
        (if state
            (dolist (next (gethash state puz-dat))
              (setq res (+ res (puz-dfs-count1 next target)))))))
    (puthash (list state target) res puz-cache)
    res))

;; Test improved solver on part 1
(message "Solution for part 1 using solver count1 is = %S" (puz-dfs-count1 "you" "out"))

;; For part 2 we utilize that total number of solutions can be found as:
;; svr -> dac -> fft -> out + svr -> fft -> dac -> out
;; so no modifications to DFS algorithm is needed.

(message "Solution for part 2 using count1 is = %S"
         (+
          (* (puz-dfs-count1 "svr" "dac") (puz-dfs-count1 "dac" "fft") (puz-dfs-count1 "fft" "out"))
          (* (puz-dfs-count1 "svr" "fft") (puz-dfs-count1 "fft" "dac") (puz-dfs-count1 "dac" "out"))))

;; Some other and more lisp like solutions, after code review by Claude.ai
;; Properly not much efficiency, mostly for improving elisp skills

(setq puz-cache (make-hash-table :test 'equal));; New and clean cache

(defun puz-dfs-count2 (state target)
  "Find number of paths using DFS search from STATE to TARGET, utilizes `puz-cache'."
  (if (equal state target)
      1
    (or (gethash (list state target) puz-cache)
        (let ((acc 0))
        (dolist (next (gethash state puz-dat))
          (cl-incf acc (puz-dfs-count2 next target)))
        (puthash (list state target) acc puz-cache)
        acc))))

;; Test solver on part 1
(message "Solution for part 1 using count2 solver is = %S" (puz-dfs-count2 "you" "out"))


(setq puz-cache (make-hash-table :test 'equal));; New and clean cache

;; Even more lisp like solution, using cl-loop and no local vars, much input from Claude.ai
(defun puz-dfs-count3 (state target)
  "Find number of paths using DFS search from STATE to TARGET, utilizes `puz-cache'."
  (if (equal state target) ; target reached
      1
    (or (gethash (list state target) puz-cache) ;; part 2 is only evaluated if part 1 (cache) fails
        (puthash (list state target)
                 (cl-loop for next in (gethash state puz-dat)
                          sum (puz-dfs-count3 next target)) puz-cache))))

;; Test solver on part 1
(message "Solution for part 1 using count3 solver is = %S" (puz-dfs-count3 "you" "out"))

;; One observation is that the cache is indexed by '(list state target)'
;; For one run target is always the same, hence redundant, better solution is to just use
;; starte as index and then have a new cache per target (will also reduce size of cache)
;; This is not at all important for solving the AOC problem, but nice to explore.

(setq puz-cache (make-hash-table :test 'equal));; New and clean cache

;; Version using a local cache, only naming the state
(defun puz-dfs-count4 (state target)
    "Find number of paths using DFS search from STATE to TARGET, mush be called with `puz-cache' dynamically bound to a fresh table for this TARGET."
  (if (equal state target)
      1
    (or (gethash state puz-cache)
        (let ((acc 0))
        (dolist (next (gethash state puz-dat))
          (cl-incf acc (puz-dfs-count4 next target)))
        (puthash state acc puz-cache)
        acc))))

(defun puz-solve-atob4 (start target)
  "Solver from START to TARGET using let binding of special variabel `puz-cache'."
  (let ((puz-cache (make-hash-table :test 'equal)))  ; Make new "local special var"
    (puz-dfs-count4 start target)))

;; Test solver on part 1
(message "Solution for part 1 using atob4 solver is = %S" (puz-solve-atob4 "you" "out"))

;; Another approach inspired by Claude
;; Advanced function that outputs a counter fuction

(defun puz-make-counter (target)
  "Return a solver function for TARGET."
  (let ((cache (make-hash-table :test 'equal)))
    (cl-labels ((countit (state)
                    (if (equal state target)
                        1
                      (or (gethash state cache)
                          (let ((acc 0))
                            (dolist (next (gethash state puz-dat))
                              (cl-incf acc (countit next)))
                            (puthash state acc cache)
                            acc)))))
      #'countit)))

(defvar puz-dfs-count5)
(setq puz-dfs-count5 (puz-make-counter "out"))
;; Test solver on part 1
(message "Solution for part 1 using puz-dfs-count5 solver is = %S" (funcall puz-dfs-count5 "you"))

;; Some benchmarking for testing performance, but for AOC all solution with cache is very fast

(defun puz-solve2 ()
  "Test solver for benchmark."
  (setq puz-cache (make-hash-table :test 'equal))
  (+
   (* (puz-dfs-count2 "svr" "dac") (puz-dfs-count2 "dac" "fft") (puz-dfs-count2 "fft" "out"))
   (* (puz-dfs-count2 "svr" "fft") (puz-dfs-count2 "fft" "dac") (puz-dfs-count2 "dac" "out")))
  )

(benchmark-run 100 (puz-solve2))

(defun puz-solve3 ()
  "Test solver for benchmark."
  (setq puz-cache (make-hash-table :test 'equal))
   (+
   (* (puz-dfs-count3 "svr" "dac") (puz-dfs-count3 "dac" "fft") (puz-dfs-count3 "fft" "out"))
   (* (puz-dfs-count3 "svr" "fft") (puz-dfs-count3 "fft" "dac") (puz-dfs-count3 "dac" "out")))
  )

(benchmark-run 100 (puz-solve3))

;;; puz_11.el ends here
