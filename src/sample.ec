require import AllCore IntDiv CoreMap List Distr.

from Jasmin require import JModel_x86.

import SLH64.

module M = {
  proc sample_f (n:W64.t, buf:W64.t) : W64.t = {
    var result:W64.t;
    var bytepos:W64.t;
    var bitpos:W64.t;
    var mask:W64.t;
    var all1:W64.t;
    var addr:W64.t;
    var b:W64.t;
    var a0:W64.t;
    var i:W64.t;
    var n_minus_1:W64.t;
    var bit:W64.t;
    var an1:W64.t;
    var sign:W64.t;
    var magnitude:W64.t;
    bytepos <- (W64.of_int 0);
    bitpos <- (W64.of_int 0);
    mask <- (W64.of_int 1);
    all1 <- (W64.of_int 1);
    addr <- bytepos;
    addr <- (addr * (W64.of_int 8));
    addr <- (addr + buf);
    b <- (loadW64 Glob.mem (W64.to_uint addr));
    a0 <- b;
    a0 <- (a0 `&` mask);
    mask <- (mask + mask);
    bitpos <- (bitpos + (W64.of_int 1));
    if ((bitpos = (W64.of_int 64))) {
      bitpos <- (W64.of_int 0);
      bytepos <- (bytepos + (W64.of_int 1));
      mask <- (W64.of_int 1);
    } else {
      
    }
    i <- (W64.of_int 1);
    n_minus_1 <- n;
    n_minus_1 <- (n_minus_1 - (W64.of_int 1));
    while ((i \ult n_minus_1)) {
      addr <- bytepos;
      addr <- (addr * (W64.of_int 8));
      addr <- (addr + buf);
      b <- (loadW64 Glob.mem (W64.to_uint addr));
      bit <- b;
      bit <- (bit `&` mask);
      mask <- (mask + mask);
      bitpos <- (bitpos + (W64.of_int 1));
      if ((bitpos = (W64.of_int 64))) {
        bitpos <- (W64.of_int 0);
        bytepos <- (bytepos + (W64.of_int 1));
        mask <- (W64.of_int 1);
      } else {
        
      }
      if ((bit <> (W64.of_int 0))) {
        all1 <- (W64.of_int 0);
      } else {
        
      }
      i <- (i + (W64.of_int 1));
    }
    addr <- bytepos;
    addr <- (addr * (W64.of_int 8));
    addr <- (addr + buf);
    b <- (loadW64 Glob.mem (W64.to_uint addr));
    an1 <- b;
    an1 <- (an1 `&` mask);
    sign <- an1;
    sign <- (sign + sign);
    sign <- (sign - (W64.of_int 1));
    magnitude <- (W64.of_int 1);
    magnitude <- (magnitude - a0);
    bit <- all1;
    bit <- (bit + bit);
    magnitude <- (magnitude + bit);
    result <- sign;
    result <- (result * magnitude);
    return result;
  }
}.
