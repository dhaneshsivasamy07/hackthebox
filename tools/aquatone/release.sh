#!/bin/bash

CURRENT_VERSION=$(cat core/banner.go | grep Version | cut -d '"' -f 2)
TO_UPDATE=(
    core/banner.go
)

read -p "[?] Did you remember to update CHANGELOG.md? "
read -p "[?] Did you remember to update README.md with new features/changes? "

echo -n "[*] Current version is $CURRENT_VERSION. Enter new version: "
read NEW_VERSION
echo "[*] Pushing and tagging version $NEW_VERSION in 5 seconds..."
sleep 5

for file in "${TO_UPDATE[@]}"
do
  echo "[*] Patching $file ..."
  sed -i".bak" "s/$CURRENT_VERSION/$NEW_VERSION/g" $file
  rm core/banner.go.bak
  git add $file
done

git commit -m "Releasing v$NEW_VERSION"
git push

git tag -a v$NEW_VERSION -m "Release v$NEW_VERSION"
git push origin v$NEW_VERSION

echo
echo "[*] All done, v$NEW_VERSION released."
