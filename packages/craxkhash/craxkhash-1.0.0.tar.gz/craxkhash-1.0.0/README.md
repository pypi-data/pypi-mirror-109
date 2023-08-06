# Craxk
## What is Craxk ?
Craxk is a **UNIQUE AND NON-REPLICABLE** Hash that uses data from the hardware where it is executed to form a hash that can only be reproduced by a single machine. That is, each Craxk hash is totally **UNIQUE** and impossible to break through a Reverse from a machine other than the host.

## How is Craxk formed ?
The hash is formed using as part of the Shake and Blake working together. In addition, each hash uses unique and altered information from the hardware as mutants of the final hash.

Crack allows you to work with different amounts of bits:
* Craxk 128
* Craxk 256
* Craxk 512

It is very important to emphasize that Craxk is not intended to be a quick hash, far from it. On the contrary, this is a considerably slower hash than the rest.                 
Craxk is a hash that points towards security, trying to prioritize security above all by applying a new variant to the function (Hardware Information).                         
If you are looking for a fast hashing function, Craxk is certainly not for you. In that case I would recommend xxhash.

## Usage 

### Class
Craxk is organized in classes. These classes work to define what kind of hash you want to use.

Classes are:
* craxk_128
* craxk_128_datemutation
* craxk_128_seedmutation
* craxk_256
* craxk_256_datemutation
* craxk_256_seedmutation
* craxk_512
* craxk_512_datemutation
* craxk_512_seedmutation

From here all the arguments that are used could be explicit in bytes, string, or int.

`craxk_128(data)`

This is the class belonging to the 128-bit main hash, which uses only non-repeatable hardware information as a mutation.

`craxk_128_datemutation(data)`

This is the class belonging to the 128-bit hash in which you add the date mutation.
What this means is that the hash will be mutated with non-replicable information from the hardware and also with the data of the current system date.
The great utility of datemutation is to be able to create a hash that can only be replicated by the same hardware and on the same date.

For example: The hash of the string `Hello World` on machine 1 on 06/16/2021 will not be the same as the hash of the same string on 06/17/2021.

Without a doubt, datemutation opens a range of possibilities

`craxk_128_seedmutation(data, seed=)`

This is the class belonging to the 128-bit hash in which you add the mutation of a seed.
What this means is that the hash will be mutated with non-replicable hardware information and also with the seed that you enter

seedmutation offers the possibility that the hash can only be obtained again by generating it from the same machine and with the specified seed.

The seed must not be a white space and can also be bytes, string, int or float




### Functions

`hash.update(data)`

Update the hash object. Repeated calls are equivalent to a single call with the concatenation of all the arguments: `m.update(a)`; `m.update(b)` is equivalent to `m.update(a+b)`. In the case of seedmutation, only the data is updated, the seed will remain the same as before.



`hash.replace()`

Similary to update() only this function replaces the data and does not concatenate it like update() would.
In the case of seedmutation, here you will need to specify the seed again using the `seed=` argument.



`hash.digest()`

Return the digest of the data. This is a bytes object of size digest_size which may contain bytes in the whole range from 0 to 255.

For example, to obtain the digest of the byte string `b'Nobody inspects the spammish repetition'`:

**Input**
```python
import craxkhash
x = craxhhash.craxk_128()
x.update(b'Nobody inspects')
x.update(b' the spammish repetition')
x.digest()
```
**Output**
```console
> b'R\xda\xbe \x9a-\xb0&p\x07\x8e\xb2\xdb\x8b\x02N'
```




`hash.hexdigest()`
It is the same as digest (), only the digest is returned as a double-length string object that only contains hexadecimal digits.

For example, to obtain the hexdigest of the byte string `b'Nobody inspects the spammish repetition'`:

```python
import craxkhash
x = craxhhash.craxk_128()
x.update(b'Nobody inspects')
x.update(b' the spammish repetition')
x.hexdigest()
```
**Output**
```console
> 52dabe209a2db02670078eb2db8b024e
```




`hash.digest_size`

The size of the resulting hash in bytes.




`hash.block_size`

The internal block size of the hash algorithm in bytes.


## Other information

Crack works in Python versions 2.7 onwards.

Currently only native Python libraries are used.

Those libraries are:
* os
* hashlib
* subprocess
* uuid
* time
* base64

**It is very important to emphasize that this project is created by a programming enthusiast, in addition to the fact that the project is in continuous development**