#!/bin/sh

defaults write com.apple.ncprefs content_visibility -int 2  # notif previews only when unlocked


# Dock
# ====

defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock mru-spaces -bool false # do not rearrange spaces
defaults write com.apple.dock persistent-apps -array
defaults write com.apple.dock show-recents -bool false
defaults write com.apple.dock showAppExposeGestureEnabled -bool false
defaults write com.apple.dock tile-size -int 64
defaults write com.apple.dock expose-group-apps -bool true

# disable hot corners
defaults write com.apple.dock wvous-bl-corner -int 0
defaults write com.apple.dock wvous-br-corner -int 0
defaults write com.apple.dock wvous-tl-corner -int 0
defaults write com.apple.dock wvous-tr-corner -int 0

killall Dock


# Finder
# ======

chflags nohidden ~/Library
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"
defaults write com.apple.finder FXRemoveOldTrashItems -bool true
defaults write com.apple.finder ShowPathbar -bool true
defaults write NSGlobalDomain AppleShowAllExtensions -bool true

defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool true
defaults write com.apple.finder ShowHardDrivesOnDesktop -bool false
defaults write com.apple.finder ShowRemovableMediaOnDesktop -bool true

killall Finder


# AirDrop
# =======

defaults write com.apple.NetworkBrowser BrowseAllInterfaces -bool true
defaults write com.apple.sharingd DiscoverableMode -string "Contacts Only"


# Siri
# ====

defaults write com.apple.assistant.support 'Siri Data Sharing Opt-In Status' -int 2  # opt out
defaults write com.apple.assistant.support "Assistant Enabled" -bool false
defaults write com.apple.SetupAssistant DidSeeSiriSetup -bool true
defaults write com.apple.Siri StatusMenuVisible -bool false
defaults write com.apple.Siri UserHasDeclinedEnable -bool true


# Track pad
# =========

defaults write com.apple.AppleMultitouchTrackpad TrackpadPinch -int 1
defaults write com.apple.AppleMultitouchTrackpad TrackpadRightClick -int 1
defaults write com.apple.AppleMultitouchTrackpad TrackpadScroll -int 1
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerHorizSwipeGesture -int 2
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerVertSwipeGesture -int 2
defaults write com.apple.AppleMultitouchTrackpad TrackpadTwoFingerFromRightEdgeSwipeGesture -int 3

# Keyboard
# ========

# Map the capslock key to escape
hidutil property --set '{"UserKeyMapping":[{"HIDKeyboardModifierMappingSrc":0x700000039,"HIDKeyboardModifierMappingDst":0x700000029}]}'
