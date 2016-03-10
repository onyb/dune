open Lwt

module Main (C: V1_LWT.CONSOLE) = struct

  let start c =
    for_lwt i = 1 to 7 do
      lwt () = OS.Time.sleep 2.0 in
      C.log c "Hello World!\n";
      return ()
    done

end
