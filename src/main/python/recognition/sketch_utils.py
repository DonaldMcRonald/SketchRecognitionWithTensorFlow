from generated_proto import sketch_pb2 as Sketch
import numpy
import uuid

def convert_array_to_points(points):
    result = []
    for row in points:
        new_point = make_point(numpy.asscalar(row[0]), numpy.asscalar(row[1]))
        result.append(new_point)
    return result

def make_point(x, y, time=0):
    new_point = Sketch.SrlPoint()
    new_point.id = str(uuid.uuid1())
    new_point.x = x
    new_point.y = y
    new_point.time = time
    return new_point

def convert_points_to_array(points, stroke):
    result = []
    for point in points:
        result.append([point.x, point.y, stroke.id])
    return result

def strip_ids_from_points(points):
    ID = 2
    for point in points:
        point.pop(ID)

def create_points_from_shape(shape):
    ''' Creates random point list
        Basically what this does is create a list of points or a list of lists of points based on random values.'''
    def stroke_func(points, stroke):
        return convert_points_to_array(points, stroke), stroke

    def shape_func(sub_calls_results, shape):
        """converts list_o_points into a list of lists of points potentially... randomly merging points too"""
        result = []
        #for now lets just merge them all!

        for object in sub_calls_results:
            result.extend(object[0])
        return result, shape

    return call_shape_recursively(stroke_func=stroke_func, shape_func=shape_func, srl_object=shape)[0]

def call_shape_recursively(srl_object, stroke_func, shape_func, finished_func=None, top=True):
    ''' calls the objects recursively and calls stroke_func on strokes and then calls a shape_func on the list of results and the shape'''
    values_of_results = []
    shape = None
    if srl_object.DESCRIPTOR.name == "SrlShape":
        shape = srl_object
    else:
        object = srl_object.object
        type = srl_object.type
        if type == Sketch.SHAPE:
            shape = Sketch.SrlShape()
            shape.ParseFromString(object)
        elif type == Sketch.STROKE:

            stroke = Sketch.SrlStroke()
            stroke.ParseFromString(object)
            return stroke_func(stroke.points, stroke)

        return shape_func(values_of_results, shape=shape)
    for sub_object in shape.subComponents:
        values_of_results.append(call_shape_recursively(stroke_func=stroke_func, shape_func=shape_func,
                                                             finished_func=finished_func, srl_object=sub_object, top=False))

    if top and finished_func is not None:
        return finished_func(shape_func(values_of_results, shape), shape)
    return shape_func(values_of_results, shape)
