/*

Copyright (C) 2003-2009 Kevin Thornton, krthornt[]@[]uci.edu

Remove the brackets to email me.

This file is part of libsequence.

libsequence is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

libsequence is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
long with libsequence.  If not, see <http://www.gnu.org/licenses/>.

*/

#ifndef COMPARISONS_H
#define COMPARISONS_H
/*! \file Comparisons.hpp
  @brief delcaration of routines for comparing DNA sequences
  This file declares a set of functions useful for comparing two bits
  of sequence data--sequences, nucleotides, etc.
 
  @short Routines to compare bases, sequences, etc. 
  Declares Sequence::TsTv,Sequence::NumDiffs,Sequence::Gapped,
  Sequence::NotAGap
  \ingroup misc
*/

#include <string>
#include <algorithm>
#include <type_traits>
#include <Sequence/SeqEnums.hpp>

namespace Sequence
{
  Mutations TsTv(const char & i, const char & j);
  Mutations TsTv(const int & i,const int & j);
  bool Different (const std::string & seq1,
		  const std::string & seq2,
		  const bool & skip_missing = true,
		  const bool & nucleic_acid = true);
  
  int NumDiffs(const std::string & seq1,
	       const std::string & seq2,
	       const bool & skip_missing = true ,
	       const bool & nucleic_acid = true);

  bool Gapped(const std::string &s);

  template<typename Iterator> bool Gapped(Iterator beg,Iterator end,
					  const char & gapchar = '-')
    /*!
      \param beg an iterator
      \param end an iterator
      \param gapchar a character representing an aligment gap
      \return true if \a gapchar is present in the range [beg,end), false otherwise
    */
  {
    Iterator itr = std::find(beg,end,gapchar);
    return (itr!=end);
  }

  bool NotAGap(const char &c);
}
#endif
