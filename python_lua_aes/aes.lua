local aes = require "resty.aes"

local iv = "78afc8512559b62f"
local key = "78afc8512559b62f"
local text = "c6d1965bf800d5f7682636826c9a097e"

local aes_128_cbc_with_iv = assert(aes:new(key, nil, aes.cipher(128, "cbc"), {iv=iv, method=nil}))
local encrypted = ngx.encode_base64(aes_128_cbc_with_iv:encrypt(text))

ngx.say("#####encrypted: " .. encrypted)
ngx.say("#####decrypted: " .. aes_128_cbc_with_iv:decrypt(ngx.decode_base64(encrypted)))
