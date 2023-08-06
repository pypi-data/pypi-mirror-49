//! \file Sequence/samflag.hpp @brief SAM flags
#ifndef __LIBSEQ_SAMFLAG_HPP__
#define __LIBSEQ_SAMFLAG_HPP__

#include <iosfwd>
#include <cstdio>
#include <cstdint>
namespace Sequence
{
  /*!
    \namespace Sequence::sambits

    \brief Stores the hex flags used by a SAM file flag field in an easy-to-read format

    \ingroup HTS
  */
  namespace sambits
  {
    static const int is_paired=0x0001;
    static const int is_proper_pair=0x0002;
    static const int query_unmapped=0x0004;
    static const int mate_unmapped=0x0008;
    static const int qstrand = 0x0010;
    static const int mstrand = 0x0020;
    static const int first_read = 0x0040;
    static const int second_read = 0x0080;
    static const int not_primary = 0x0100;
    static const int qcfail = 0x0200;
    static const int duplicate = 0x0400;
    static const int suppalign = 0x0800;  //Supplementary alignment
  }

  /*!
    \class Sequence::samflag Sequence/samflag.hpp
    \brief The flag field of a SAM record
    
    A SAM file's FLAG field is stored as an integer that is the sum of
    a series of flags (defined in namespace Sequence::sambits).

    This class simply takes that integer and stores a set of boolean 
    variables based on the value of the integer.
  */
  class samflag
  {
  private:
    void process_bits();
  public:
    /*!
      The flag value
    */
    std::int32_t flag;
    bool is_paired,is_proper_pair,query_unmapped,
      mate_unmapped,qstrand,mstrand,first_read,
      second_read,not_primary,qcfail,duplicate,supp_alignment;
    samflag(const std::int32_t & __flag);
    samflag();
    operator std::int32_t() const;
    std::istream & read( std::istream & i);
  };

  std::ostream & operator<<(std::ostream & o, const samflag & s);
  std::istream & operator>>(std::istream & i, samflag & s);
}

#endif
