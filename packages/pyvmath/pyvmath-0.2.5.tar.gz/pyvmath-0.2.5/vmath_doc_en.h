
PyDoc_STRVAR(vec2_doc, 
	"a 2-D vector in array-of-structures format");

PyDoc_STRVAR(vec3_doc, 
	"a 3-D vector in array-of-structures format");

PyDoc_STRVAR(vec4_doc, 
	"a 4-D vector in array-of-structures format");

PyDoc_STRVAR(quat_doc, 
	"a quaternion in array-of-structures format");

PyDoc_STRVAR(mat22_doc, 
	"a 2x2 matrix in array-of-structures format");

PyDoc_STRVAR(mat33_doc, 
	"a 3x3 matrix in array-of-structures format");

PyDoc_STRVAR(mat44_doc, 
	"a 4x4 matrix in array-of-structures format");

//add
PyDoc_STRVAR(add_doc,
	"add two vectors or two matrices\n"\
	"\n"\
	"c = pyvmath.add(a, b)");
//sub
PyDoc_STRVAR(sub_doc,
	"sub two vectors or two matrices\n"\
	"\n"\
	"c = pyvmath.sub(a, b)");
//mul
PyDoc_STRVAR(mul_doc,
	"multiply 2 elements  \n"\
	"\n"\
	"c = pyvmath.mul(a, b) \n"\
	"\n"\
	"the following combinations are possible\n"\
	"\n"\
	"vector = vector x scalar\n"\
	"matrix = matrix x scalar\n"\
	"vector = matrix x vector (transform vector)\n"\
	"matrix = matrix x matrix\n"\
	"quatanion = quatanion x quatanion\n"\
	"vector = vector * vector (multiply per element)\n");
//div
PyDoc_STRVAR(div_doc,
	"division vector by a scalar\n"\
	"\n"\
	"vector = pyvmath.div(vector, scalar)\n"\
	"\n"\
	"division vector per element\n"\
	"\n"\
	"vector = pyvmath.div(vector, vector)");

//recip
PyDoc_STRVAR(recip_doc,
	"compute the reciprocal of a vector per element\n"\
	"\n"\
	"vector = pyvmath.recip(vector)");

//sqrt
PyDoc_STRVAR(sqrt_doc,
	"compute the square root of a vector per element\n"\
	"\n"\
	"vector = pyvmath.sqrt(vector)");

//rsqrt
PyDoc_STRVAR(rsqrt_doc,
	"compute the reciprocal square root of a vector per element\n"\
	"\n"\
	"vector = pyvmath.rsqrt(vector)");

//abs
PyDoc_STRVAR(abs_doc,
	"compute the absolute value of a vector per element\n"\
	"\n"\
	"vector = pyvmath.abs(vector)");

//max
PyDoc_STRVAR(max_doc,
	"maximum element of a vector\n"\
	"\n"\
	"scalar = pyvmath.max(vector)");

//min
PyDoc_STRVAR(min_doc,
	"minimum element of a vector\n"\
	"\n"\
	"scalar = pyvmath.min(vector)");

//maxElem
PyDoc_STRVAR(maxElem_doc,
	"maximum of two vectors per element\n"\
	"\n"\
	"vector = pyvmath.matElem(vector,vector)");

//minElem
PyDoc_STRVAR(minElem_doc,
	"minimum of two vectors per element\n"\
	"\n"\
	"vector = pyvmath.minElem(vector, vector)");

//sum
PyDoc_STRVAR(sum_doc,
	"compute the sum of all elements of a vector\n"\
	"\n"\
	"scalar = pyvmath.sum(vector)");

//dot
PyDoc_STRVAR(dot_doc,
	"compute the dot product of two vectors\n"\
	"\n"\
	"scalar = pyvmath.dot(vector, vector)");

//lengthSqr
PyDoc_STRVAR(lengthSqr_doc,
	"compute the square of the length of a vector\n"\
	"\n"\
	"scalar = pyvmath.lengthSqr(vector)");

//length
PyDoc_STRVAR(length_doc,
	"compute the length of a vector\n"\
	"\n"\
	"scalar = pyvmath.length(vector)");

//normalize
PyDoc_STRVAR(normalize_doc,
	"normalize a vector\n"\
	"\n"\
	"vector = pyvmath.normalize(vector)");

//cross
PyDoc_STRVAR(cross_doc,
	"compute cross product of two vectors\n"\
	"\n"\
	"scalar = pyvmath.cross(vec2, vec2)\n"\
	"vec3 = pyvmath.cross(vec3, vec3)");

//lerp
PyDoc_STRVAR(lerp_doc,
	"linear interpolation between two vectors\n"\
	"\n"\
	"vector = pyvmath.lerp(t, vector, vector)  (0<= t <= 1)");

//slerp
PyDoc_STRVAR(slerp_doc,
	"spherical linear interpolation between two vectors\n"\
	"\n"\
	"vector = pyvmath.slerp(t, vector, vector)  (0<= t <= 1)");

//quat_rotation
PyDoc_STRVAR(quat_rotation_doc,
	"construct a quaternion\n"\
	"\n"\
	"quat = pyvmath.quat_rotation(vec3, vec3)\n"\
	"\n"\
	"construct a quaternion to rotate between two unit - length 3D vectors\n"\
	"the result is unpredictable if 2 vectors point in opposite directions\n"\
	"\n"\
	"quat = pyvmath.quat_rotation(scalar, vec3)\n"\
	"\n"\
	"construct a quaternion to rotate around a unit-length 3D vector\n"\
	"\n"\
	"quat = pyvmath.quat_rotation(scalar)\n"\
	"\n"\
	"construct a quaternion to rotate around a Z(0,0,1) axis");

	//quat_rotationX
PyDoc_STRVAR(quat_rotationX_doc,
	"construct a quaternion to rotate around the x axis\n"\
	"\n"\
	"quat = pyvmath.quat_rotationX(radian)");

//quat_rotationY
PyDoc_STRVAR(quat_rotationY_doc,
	"construct a quaternion to rotate around the y axis\n"\
	"\n"\
	"quat = pyvmath.quat_rotationY(radian)");

//quat_rotationZ
PyDoc_STRVAR(quat_rotationZ_doc,
	"construct a quaternion to rotate around the z axis\n"\
	"\n"\
	"quat = pyvmath.quat_rotationZ(radian)");

//conj
PyDoc_STRVAR(conj_doc,
	"compute the conjugate of a quaternion\n"\
	"\n"\
	"quat = pyvmath.conj(quat)");

//squad
PyDoc_STRVAR(squad_doc,
	"spherical quadrangle interpolation\n"\
	"\n"\
	"quat = pyvmath.squad(t,quat, quat, quat, quat)");

//rotate
PyDoc_STRVAR(rotate_doc,
	"use a unit - length quaternion to rotate a 3D vector\n"\
	"\n"\
	"vec = pyvmath.rotate(vec, quat)");

//mat_rotation
PyDoc_STRVAR(mat_rotation_doc,
	"construct a matrix to rotate around a unit-length 3D vector\n"\
	"\n"\
	"matrix = pyvmath.mat_rotation(radian, dimension, vector)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix\n"\
	"if you omit vector, Zaxis(0,0,1) will be entered as default");

//mat_rotationX
PyDoc_STRVAR(mat_rotationX_doc,
	"construct a matrix to rotate around the Xaxis\n"\
	"\n"\
	"matrix = pyvmath.mat_rotationX(radian, dimension)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationY
PyDoc_STRVAR(mat_rotationY_doc,
	"construct a matrix to rotate around the Yaxis\n"\
	"\n"\
	"matrix = pyvmath.mat_rotationY(radian, dimension)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationZ
PyDoc_STRVAR(mat_rotationZ_doc,
	"construct a matrix to rotate around the Zaxis\n"\
	"\n"\
	"matrix = pyvmath.mat_rotationZ(radian, dimension)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationZYX
PyDoc_STRVAR(mat_rotationZYX_doc,
	"construct a matrix to rotate around the x, y, and z axes\n"\
	"\n"\
	"matrix = pyvmath.mat_rotationZYX( (xradian, yradian, zradian) )");

//mat_identity
PyDoc_STRVAR(mat_identity_doc,
	"construct an identity matrix\n"\
	"\n"\
	"matrix = pyvmath.mat_identity(dimension)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix");

//mat_scale
PyDoc_STRVAR(mat_scale_doc,
	"construct a matrix to perform scaling\n"\
	"\n"\
	"matrix = pyvmath.mat_scale(vector, dimension)\n"\
	"\n"\
	"dimension is 2 or 3 or 4 to output matrix");

//mat_translation
PyDoc_STRVAR(mat_translation_doc,
	"construct a 4x4 matrix to perform translation\n"\
	"\n"\
	"matrix = pyvmath.mat_translation(vector)");

//transpose
PyDoc_STRVAR(transpose_doc,
	"transpose of a matrix\n"\
	"\n"\
	"matrix = pyvmath.transpose(matrix)");

//inverse
PyDoc_STRVAR(inverse_doc,
	"compute the inverse of a matrix\n"\
	"\n"\
	"matrix = pyvmath.inverse(matrix)");


//orthoInverse
PyDoc_STRVAR(orthoInverse_doc,
	"compute the inverse of a 4x4 matrix, \n"\
	"which is expected to be an affine matrix with an orthogonal upper-left 3x3 submatrix\n"\
	"this can be used to achieve better performance than a general inverse\n"\
	"when the specified 4x4 matrix meets the given restrictions\n"\
	"\n"\
	"matrix = pyvmath.orthoInverse(matrix)");


//determinant
PyDoc_STRVAR(determinant_doc,
	"determinant of a matrix\n"\
	"\n"\
	"scalar = pyvmath.determinant(matrix)");

//appendScale
PyDoc_STRVAR(appendScale_doc,
	"append (post-multiply) a scale transformation to a matrix\n"\
	"faster than creating and multiplying a scale transformation matrix\n"\
	"\n"\
	"matrix = pyvmath.appendScale(matrix, vector)");

//prependScale
PyDoc_STRVAR(prependScale_doc,
	"prepend (pre-multiply) a scale transformation to a 4x4 matrix\n"\
	"faster than creating and multiplying a scale transformation matrix\n"\
	"\n"\
	"matrix = pyvmath.prependScale(matrix, vector)");

//lookAt
PyDoc_STRVAR(lookAt_doc,
	"construct viewing matrix based on eye position, position looked at, and up direction\n"\
	"\n"\
	"matrix4 = pyvmath.lookAt(eyeVector, lookatVector, upVector)");

//perspective
PyDoc_STRVAR(perspective_doc,
	"construct a perspective projection matrix\n"\
	"\n"\
	"matrix4 = pyvmath.perspective(fovyRadians, aspect, zNear, zFar)");

//frustum
PyDoc_STRVAR(frustum_doc,
	"construct a perspective projection matrix based on frustum\n"\
	"\n"\
	"matrix4 = pyvmath.frustum(left, right, bottom, top, zNear, zFar)  (all scalar value)");

//orthographic
PyDoc_STRVAR(orthographic_doc,
	"construct an orthographic projection matrix\n"\
	"\n"\
	"matrix4 = pyvmath.orthographic(left, right, bottom, top, zNear, zFar)  (all scalar value)");
