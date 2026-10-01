(defun fact (n)
  (declare (xargs :guard (natp n)))
  (if (zp n) 1 (* n (fact (1- n)))))

(define nat-sum ((x nat-listp))
  :returns (sum natp)
  (b* (((when (endp x)) 0)
       (rest (nat-sum (cdr x))))
    (+ (nfix (car x)) rest)))

(defun-sk has-bigger (x)
  (exists (y) (and (natp y) (< x y))))

(defthm natp-of-nat-sum ; a rule
  (implies (nat-listp x)
           (natp (nat-sum x)))
  :hints (("Goal" :in-theory (enable nat-sum))))
