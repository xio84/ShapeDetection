(deftemplate av 
    (slot number)
    (slot angle)
    (slot distance)
    (slot xAxis))

;Shape classification
(defrule triangle
    ;if vertex-number == 3 then triangle
    (vertexNum 3)
    =>
    (assert (result triangle))
    )

(defrule quadrilateral
    ;if vertex-number == 4 then quadrilateral
    (vertexNum 4)
    =>
    (assert (result quadrilateral))
    )

(defrule pentagon
    ;if vertex-number == 5 then pentagon
    (vertexNum 5)
    =>
    (assert (result pentagon))
    )

(defrule hexagon
    ;if vertex-number == 6 then triangle
    (vertexNum 6)
    =>
    (assert (result hexagon))
    )

;Triangle classification
(defrule equilateral
    (result triangle)
    (av (number 1) (angle 60))
    (av (number 2) (angle 60))
    (av (number 3) (angle 60))
    =>
    (assert (result equilateral))
    )

(defrule isosceles
    (result triangle)
    (av (number ?n1) (angle ?a1))
    (av (number ?n2&~?n1) (angle ?a1))
    =>
    (assert (result isosceles))
    )

(defrule right
    (result triangle)
    (av (angle 90))
    =>
    (assert (result right))
    )

(defrule obtuse
    (shape triangle)
    (av (angle ?a))
    (test (> ?a 90))
    =>
    (assert (result obtuse))
    )

(defrule sharp
    (shape triangle)
    (av (number 1) (angle ?a1))
    (av (number 2) (angle ?a2))
    (av (number 3) (angle ?a3))
    (test (< ?a1 90))
    (test (< ?a2 90))
    (test (< ?a3 90))
    =>
    (assert (result sharp))
    )

;Quadrilateral classification
(defrule parallelogram
    (result quadrilateral)
    (av (number ?n1) (distance ?d1))
    (av (number ?n2&~?n1) (distance ?d2))
    (av (number ?n3&~?n2&~?n1) (distance ?d3))
    (av (number ?n4&~?n3&~?n2&~?n1) (distance ?d4))
    (test (< (- ?d1 ?d2) 5))
    (test (> (- ?d1 ?d2) -5))
    (test (< (- ?d3 ?d4) 5))
    (test (> (- ?d3 ?d4) -5))
    =>
    (assert (result parallelogram))
    )

(defrule rectangle
    (result parallelogram)
    (av (number 1) (angle 90))
    (av (number 2) (angle 90))
    (av (number 3) (angle 90))
    (av (number 4) (angle 90))
    =>
    (assert (result rectangle))
    )

(defrule kite
    (result parallelogram)
    (not (result rectangle))
    =>
    (assert (result kite))
    )

;Trapezoid Classification
(defrule Trapezoid
    (result quadrilateral)
    (not (result rectangle))
    (av (number ?n1) (angle ?a1))
    (av (number ?n2&~?n1) (angle ?a2))
    (test (= (+ ?a1 ?a2) 180))
    =>
    (assert (result trapezoid))
    )

(defrule right-side
    (result trapezoid)
    (av (number ?n1) (angle 90) (xAxis ?x1))
    (av (number ?n2&~?n1) (xAxis ?x2))
    (av (number ?n3&~?n2&~?n1) (xAxis ?x3))
    (av (number ?n4&~?n3&~?n2&~?n1) (xAxis ?x4))
    (test (> ?x1 ?x2))
    (test (> ?x1 ?x3))
    (test (> ?x1 ?x4))
    =>
    (assert (result right-side))
    )

(defrule left-side
    (result trapezoid)
    (av (number ?n1) (angle 90) (xAxis ?x1))
    (av (number ?n2&~?n1) (xAxis ?x2))
    (av (number ?n3&~?n2&~?n1) (xAxis ?x3))
    (av (number ?n4&~?n3&~?n2&~?n1) (xAxis ?x4))
    (test (< ?x1 ?x2))
    (test (< ?x1 ?x3))
    (test (< ?x1 ?x4))
    =>
    (assert (result left-side))
    )

(defrule regular
    (result trapezoid)
    (av (number ?n1) (distance ?a1))
    (av (number ?n2&~?n1) (distance ?a1))
    =>
    (assert (result regular))
    )