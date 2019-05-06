import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

export function checkFace(facedata) {
  return request({
    url: '/user/faceAuth',
    method: 'post',
    data :facedata
  })
}

export function registerFace(data){
  return request({
    url: '/user/register',
    method: 'post',
    data :data
  })
}
