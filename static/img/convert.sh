for f in *.png ; do 
    [ -f "$f" ] || continue
    out="${f%.*}.webp"
    [ -f "$out" ] && continue
    cwebp "$f" -o "$out"
done

