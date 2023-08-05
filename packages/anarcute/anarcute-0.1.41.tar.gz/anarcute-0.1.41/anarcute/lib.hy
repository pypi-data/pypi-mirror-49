(do 
  (import os csv json time)
  (require [hy.extra.anaphoric [*]])
  
  
  (do "main hall"
      (deftag r[f] `(fn[&rest rest &kwargs kwargs] (~f #*(reversed rest) #**kwargs) ))
      (defn list-dict[arr key] (dict (zip (list (map (fn[x] (get x key)) arr)) arr)))
      (defmacro get-o [&rest args] `(try (get ~@(butlast args)) (except [Exception] ~(last args))))
      (deftag try[expr]`(try ~expr (except [Exception] "")))
      (defn apply-mask[obj mask] (for[(, k v) (.items obj)] (if (in k mask) (assoc obj k ((get mask k) v)))) obj)
      (setv enmask apply-mask)
      (defnmacro print-n-pass[x] `(do (print ~x) ~x))
      (defn route[obj &optional[direction None]]
        (setv direction (if direction direction (if (>= 2 (len sys.argv) (get sys.argv 1) None))))
        (if (in direction obj) ((get obj direction) #**(get sys.argv (slice 2 None))))
        ))
  (do "timey wimey"
      (defn photo-finish-fn [f] (setv start (time.time))
        (setv res (f))
        (, (- (time.time) res)))
      (defmacro photo-finish[&rest args]
        `(do (setv start (time.time))
             ~@args
             (- (time.time) start)
             ))
      (defmacro do-not-faster-than [t &rest args] 
        `(do (setv start (time.time))
             ~@args
             (setv delta (- (time.time) start))
             (if (< 0 delta) (time.sleep (min delta ~t))))))
  
  (do "common lisp"
      (defmacro car[arr] `(get ~arr 0))
      (defmacro cdr[arr] `(get ~arr (slice 1 None)))
      (defmacro defun[&rest args] `(defn ~@args))
      (defmacro setf[&rest args] `(setv ~@args)))
  (do "anarki/arc")
  (do "pseudo arki"
      `(setv T True
             F False
             N None
             s setv
             c cond
             df defn
             ds defseq))
  (do "predicates"
      (defn in-or[needles haystack] (for [n needles] (if (in n haystack) (return True))) False)
      
      )
  (do "lambda"
      (deftag map [f] `(fn[arr] (list (map ~f arr))))
      (deftag filter [f] `(fn[arr] (list (filter ~f arr))))
      (defn filter-or-keep[arr f] (setv filtered (list (filter f arr))) (if filtered filtered arr)))
  (do "csv"
      (defn load-csv [fname &optional [key None][delimiter ","]]
        (setv arr (if (os.path.isfile fname) (-> fname (open "r+") (csv.DictReader :delimiter delimiter) list (as-> it (map dict it)) list ) []))
        (setv arr (list (map dict arr)))
        (if key (do (setv obj {}) (for [row arr] (assoc obj (get row key) row)) obj) 
          arr))
      (defn tolist[&rest args] [#*args])
      (defn fieldnames[arr] (-> (+ [] #*(+ [[]] (list (map (fn[x] (-> x (.keys) list) )arr)))) set list))
      (setv *fieldnames* fieldnames)
      (defn write-csv [fname arr &optional [id None][fieldnames None]]
        (setv writer (-> fname (open "w+") (csv.DictWriter :fieldnames (if fieldnames fieldnames (*fieldnames* arr))) ))
        (writer.writeheader)
        (for [row arr] (writer.writerow row)))
      (defn write-csv-add [fname arr &kwargs kwargs] (as-> fname it (load-csv it) (+ (list it) (list 	arr)) (write-csv fname it #**kwargs))))
  (do "json"
      (defn load-json[fname] (-> fname (open "r+") json.load))
      (defn write-json[fname obj] (-> fname (open "w+") (.write (json.dumps obj)))))
  (do "jsonl"
      (defn jsonl-json[jstr] (as-> jstr it (.split it "\n")(#filter thru it) (.join "," it)  (.format "[{}]" it)))
      (defn jsonl-loads[jstr] (-> jstr jsonl-json json.loads))
      (defn jsonl-load[f] (-> f (.read) jsonl-loads))
      (defn jsonl-dumps[arr] (.join "\n" (list (map json.dumps arr))))
      (defn jsonl-add[fname item] (-> fname (open "a+") (.write (.format "{}\n" (json.dumps item))))))
  (do "typical vars"
      (setv headers {"User-Agent" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}))
  (do "string funcs/pcze"
      (defn from-between[from a b] (-> from (.split a) last (.split b) first))
      (defn replace [s obj](for [(, k v) (.items obj)] (setv s (.replace s k v))) s)
      (defn trim[s]
        (setv s (-> s (.replace "\r\n" "\n") (.replace "\n" " ")))
        (while (s.endswith " ") (setv s (get s (slice 0 -1))))
        (while (s.startswith " ") (setv s (get s (slice 1 None))))
        (while (in "  " s) (setv s (s.replace "  " " ")))
        s)
      (defn ascii[s &optional [mode "replace"]](-> s (.encode "ascii" mode) (.decode "ascii")))
      (defn leave-only[s approved] (setv res "") (for [c s] (if (in c approved) (setv res (+ res c)))) res)
      (defn dehydrate[s] (-> s trim ascii (.lower) (leave-only "qwertyuiopasdfghjklzxcvbnm")))
      (defn escape [s] (-> s (.replace "\"" "\\\"") (#%(if (in "\"" %1) (.format "\"{}\"") %1 ))))
      (defn only-pcze[s]
        (setv permitted "1234567890 qwertyuiopasdfghjklzxcvbnm.:/-\\?!"
              permitted (+ permitted "ąćęłńóśźż")
              permitted (+ permitted (.upper permitted)))
        (as-> s it (list it) (filter (fn[c] (in c permitted)) it) (list it) (.join "" it)))
      (defn remove-control[s] (re.sub "r'\p{C}'" "" s))
      (defn json_quotes_single_to_double[j] (-> j  (replace {"{'" "{\"" "':" "\":" ", '" ", \"" ": '" ": \"" "'}" "\"}" "'," "\"," "']" "\"]" "['" "[\""})))
      (setv json-q-qq json_quotes_single_to_double))
  (do "selectors" "BROKEN get-mass"
      (defn get-mass[obj fields] (setv res {}) (for [field fields] (if (in field obj) (assoc res field (get obj field)))) res)
      (defn select [arr fields] (list (map (fn[obj] (get-mass obj fields)) arr)))
      
      
      (defn first-that [arr f] (for [elem arr] (if (f elem) (return elem))) None)
      (defmacro last-that [arr f] `(first-that (reversed ~arr) ~f))
      (defn distinct [arr f] (setv res {}) (for [row arr] (assoc res (f row) row)) res)
      (defn get-as[what structure]
        (setv obj {})
        (for [(, k v) (.items structure)]
          (assoc obj k (get what v)))
        obj)
      
      (defn sum-by[arr key]
        (setv sum 0)
        (for [row arr] (+= sum (key row)))
        sum)
      (defn pareto[data coeff key]
        (setv data (sorted data :key key :reverse True))
        
        (setv total (sum-by data key))
        
        
        (for [i (range 1 (len data))]
          (setv sub-data (get data (slice 0 i)))
          (setv sub-total (sum-by sub-data key))
          (if (> sub-total (* coeff total))
            (return sub-data))))
      (defn unique[arr &optional[key None]] (if key 
                                              (do
                                                (setv obj {})
                                                (for [elem arr]
                                                  (assoc obj (key elem) elem))
                                                (.values obj))
                                              (-> arr set list)))
      (defn thru[x] x)
      (defn apply-to-chunks[f arr size &optional [process thru]] "rework it - [[] []]"
        (setv buffer [] results []) 
        (while arr
          (buffer.append (arr.pop))
          (if (or (>= (len buffer) size) (not arr)) (do (results.append (f buffer))(setv buffer []))))
        
        (process results))
      )
  
  )
