# -*- coding: utf-8 -*- #
# frozen_string_literal: true

module Rouge
  module Lexers
    class Stata < RegexLexer
      title 'Stata'
      desc "Stata Statistical Programming Language"
      tag 'stata'
      filenames '*.do', '*.ado'
      mimetypes 'text/x-stata', 'application/x-stata'

      def self.keywords
        # Many of these keywords should really be broken up into
        # further control flow statements, but for a first pass
        # this gets us there!
        @keywords ||= Set.new %w(
          while
          forv forva forval forvalu forvalue forvalues continue
          if else gl glo glob globa global
          loc loca local
          tempfile tempvar tempname
          foreach in of
          var varl varli varlis varlist
          new newl newli nelis newlist
          num numl numli numlis numlist
          sca scal scala scalar
          de def defi defin define
          drop di dir l li lis list
          qui quie quiet quietl quietly
          noi nois noisi noisil noisily
          by bys byso bysor bysort
          help search do ado update adoupdate
          pwd cd save use append merge compress
          import edit describe codebook
          list browse count inspect table tabulate summarize
          generate replace egen rename clear
          drop keep sort encode decode order reshape
          log notes display
          set more ssc
        )
      end

      state :whitespace do
        # Force the lexer to restart for whitespace at the start of each line
        rule %r/^\s*\*.*$\n?/, Comment::Single
        rule %r/[^\S\r\n]+/, Text
        rule %r(//.*?$), Comment::Single
        rule %r(/[*].*?[*]/)m, Comment::Multiline
        #rule %r/\n+/, Text
      end

      state :operators do
        # These don't themselves require breaks at the moment. Probably should fix
        rule %r/-|\^|\*|\+/, Operator                       # Arithmetic operators
        rule %r/(?<![a-zA-Z.])\/(?![a-zA-Z.]|$)/, Operator  # Division operator (don't match path)
        rule %r/\&|\||!|~/, Operator                        # Logical operators
        rule %r/<\=?|>\=?|\=\=?|!\=|~\=/, Operator          # Comparison operators
      end

      state :string do
        rule %r/[^\\"]+/, Str::Double
        rule %r/\\./, Str::Escape
        rule %r/"/, Str::Double, :pop!
      end

      state :root do
        mixin :whitespace
        mixin :operators

        rule %r/"/, Str::Double, :string
        rule %r/(`)(.*)(')/ do
          groups Punctuation, Str::Interpol, Punctuation
        end

        rule %r/a-z:\\\/{}/i do |m|
          if self.class.keywords.include? m[0]
            token Keyword
          else
            token Name
          end
        end

      end
    end
  end
end
