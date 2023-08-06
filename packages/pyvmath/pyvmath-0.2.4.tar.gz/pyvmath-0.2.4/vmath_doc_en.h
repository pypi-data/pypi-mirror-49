
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
	"add two vectors or two matrices\n"
	"c = add(a, b)");
//sub
PyDoc_STRVAR(sub_doc,
	"sub two vectors or two matrices\n"
	"c = sub(a, b)");
//mul
PyDoc_STRVAR(mul_doc,
	"multiply 2 elements  \n"
	"c = mul(a, b) \n"
	"the following combinations are possible\n"
	"vector = vector x scalar\n"
	"matrix = matrix x scalar\n"
	"vector = matrix x vector (transform vector)\n"
	"matrix = matrix x matrix\n"
	"quatanion = quatanion x quatanion\n"
	"vector = vector * vector (multiply per element)\n");
//div
PyDoc_STRVAR(div_doc,
	"division vector by a scalar\n"
	"vector = div(vector, scalar)\n"
	"division vector per element\n"
	"vector = div(vector, vector)");

//recip
PyDoc_STRVAR(recip_doc,
	"compute the reciprocal of a vector per element\n"
	"vector = recip(vector)");

//sqrt
PyDoc_STRVAR(sqrt_doc,
	"compute the square root of a vector per element\n"
	"vector = sqrt(vector)");

//rsqrt
PyDoc_STRVAR(rsqrt_doc,
	"compute the reciprocal square root of a vector per element\n"
	"vector = rsqrt(vector)");

//abs
PyDoc_STRVAR(abs_doc,
	"compute the absolute value of a vector per element\n"
	"vector = abs(vector)");

//max
PyDoc_STRVAR(max_doc,
	"maximum element of a vector\n"
	"scalar = max(vector)");

//min
PyDoc_STRVAR(min_doc,
	"minimum element of a vector\n"
	"scalar = min(vector)");

//maxElem
PyDoc_STRVAR(maxElem_doc,
	"maximum of two vectors per element\n"
	"vector = matElem(vector,vector)");

//minElem
PyDoc_STRVAR(minElem_doc,
	"minimum of two vectors per element\n"
	"vector = minElem(vector, vector)");

//sum
PyDoc_STRVAR(sum_doc,
	"compute the sum of all elements of a vector\n"
	"scalar = sum(vector)");

//dot
PyDoc_STRVAR(dot_doc,
	"compute the dot product of two vectors\n"
	"scalar = dot(vector, vector)");

//lengthSqr
PyDoc_STRVAR(lengthSqr_doc,
	"compute the square of the length of a vector\n"
	"scalar = lengthSqr(vector)");

//length
PyDoc_STRVAR(length_doc,
	"compute the length of a vector\n"
	"scalar = length(vector)");

//normalize
PyDoc_STRVAR(normalize_doc,
	"normalize a vector\n"
	"vector = normalize(vector)");

//cross
PyDoc_STRVAR(cross_doc,
	"compute cross product of two vectors\n"
	"scalar = cross(vec2, vec2)\n"
	"vec3 = cross(vec3, vec3)");

//lerp
PyDoc_STRVAR(lerp_doc,
	"linear interpolation between two vectors\n"
	"vector = lerp(t, vector, vector)  (0<= t <= 1)");

//slerp
PyDoc_STRVAR(slerp_doc,
	"spherical linear interpolation between two vectors\n"
	"vector = slerp(t, vector, vector)  (0<= t <= 1)");

//quat_rotation
PyDoc_STRVAR(quat_rotation_doc,
	"construct a quaternion\n"
	"quat = quat_rotation(vec3, vec3)\n"
	"construct a quaternion to rotate between two unit - length 3D vectors\n"
	"the result is unpredictable if 2 vectors point in opposite directions\n"
	"quat = quat_rotation(scalar, vec3)\n"
	"construct a quaternion to rotate around a unit-length 3D vector\n"
	"quat = quat_rotation(scalar)\n"
	"construct a quaternion to rotate around a Z(0,0,1) axis");

	//quat_rotationX
PyDoc_STRVAR(quat_rotationX_doc,
	"construct a quaternion to rotate around the x axis\n"
	"quat = quat_rotationX(radian)");

//quat_rotationY
PyDoc_STRVAR(quat_rotationY_doc,
	"construct a quaternion to rotate around the y axis\n"
	"quat = quat_rotationY(radian)");

//quat_rotationZ
PyDoc_STRVAR(quat_rotationZ_doc,
	"construct a quaternion to rotate around the z axis\n"
	"quat = quat_rotationZ(radian)");

//conj
PyDoc_STRVAR(conj_doc,
	"compute the conjugate of a quaternion\n"
	"quat = conj(quat)");

//squad
PyDoc_STRVAR(squad_doc,
	"spherical quadrangle interpolation\n"
	"quat = squad(t,quat, quat, quat, quat)");

//rotate
PyDoc_STRVAR(rotate_doc,
	"use a unit - length quaternion to rotate a 3D vector"
	"vec = rotate(vec, quat)");

//mat_rotation
PyDoc_STRVAR(mat_rotation_doc,
	"construct a matrix to rotate around a unit-length 3D vector\n"
	"matrix = mat_rotation(radian, dimension, vector)\n"
	"dimension is 2 or 3 or 4 to output matrix\n"
	"if you omit vector, Zaxis(0,0,1) will be entered as default");

//mat_rotationX
PyDoc_STRVAR(mat_rotationX_doc,
	"construct a matrix to rotate around the Xaxis\n"
	"matrix = mat_rotationX(radian, dimension)\n"
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationY
PyDoc_STRVAR(mat_rotationY_doc,
	"construct a matrix to rotate around the Yaxis\n"
	"matrix = mat_rotationY(radian, dimension)\n"
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationZ
PyDoc_STRVAR(mat_rotationZ_doc,
	"construct a matrix to rotate around the Zaxis\n"
	"matrix = mat_rotationZ(radian, dimension)\n"
	"dimension is 2 or 3 or 4 to output matrix");

//mat_rotationZYX
PyDoc_STRVAR(mat_rotationZYX_doc,
	"construct a matrix to rotate around the x, y, and z axes\n"
	"matrix = mat_rotationZYX( (xradian, yradian, zradian) )");

//mat_identity
PyDoc_STRVAR(mat_identity_doc,
	"construct an identity matrix\n"
	"matrix = mat_identity(dimension)\n"
	"dimension is 2 or 3 or 4 to output matrix");

//mat_scale
PyDoc_STRVAR(mat_scale_doc,
	"construct a matrix to perform scaling\n"
	"matrix = mat_scale(vector, dimension)\n"
	"dimension is 2 or 3 or 4 to output matrix");

//mat_translation
PyDoc_STRVAR(mat_translation_doc,
	"construct a 4x4 matrix to perform translation\n"
	"matrix = mat_translation(vector)");

//transpose
PyDoc_STRVAR(transpose_doc,
	"transpose of a matrix\n"
	"matrix = transpose(matrix)");

//inverse
PyDoc_STRVAR(inverse_doc,
	"compute the inverse of a matrix\n"
	"matrix = inverse(matrix)");


//orthoInverse
PyDoc_STRVAR(orthoInverse_doc,
	"compute the inverse of a 4x4 matrix, which is expected to be an affine matrix with an orthogonal upper-left 3x3 submatrix\n"
	"this can be used to achieve better performance than a general inverse when the specified 4x4 matrix meets the given restrictions\n"
	"matrix = orthoInverse(matrix)");


//determinant
PyDoc_STRVAR(determinant_doc,
	"determinant of a matrix\n"
	"scalar = determinant(matrix)");

//appendScale
PyDoc_STRVAR(appendScale_doc,
	"append (post-multiply) a scale transformation to a matrix\n"
	"faster than creating and multiplying a scale transformation matrix\n"
	"matrix = appendScale(matrix, vector)");

//prependScale
PyDoc_STRVAR(prependScale_doc,
	"prepend (pre-multiply) a scale transformation to a 4x4 matrix\n"
	"faster than creating and multiplying a scale transformation matrix\n"
	"matrix = prependScale(matrix, vector)");

//lookAt
PyDoc_STRVAR(lookAt_doc,
	"construct viewing matrix based on eye position, position looked at, and up direction\n"
	"matrix4 = lookAt(eyeVector, lookatVector, upVector)");

//perspective
PyDoc_STRVAR(perspective_doc,
	"construct a perspective projection matrix\n"
	"matrix4 = perspective(fovyRadians, aspect, zNear, zFar)");

//frustum
PyDoc_STRVAR(frustum_doc,
	"construct a perspective projection matrix based on frustum\n"
	"matrix4 = frustum(left, right, bottom, top, zNear, zFar)  (all scalar value)");

//orthographic
PyDoc_STRVAR(orthographic_doc,
	"construct an orthographic projection matrix\n"
	"matrix4 = orthographic(left, right, bottom, top, zNear, zFar)  (all scalar value)");
