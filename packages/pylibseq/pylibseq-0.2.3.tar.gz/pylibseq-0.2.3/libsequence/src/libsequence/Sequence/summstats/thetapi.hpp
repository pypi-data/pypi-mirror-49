/*!
\file summstats/thetapi.hpp
*/
#ifndef SEQUENCE_SUMMSTATS_THETAPI_HPP__
#define SEQUENCE_SUMMSTATS_THETAPI_HPP__

#include <Sequence/AlleleCountMatrix.hpp>

namespace Sequence
{
    /*! \brief Mean pairwise differences
     * \param m An AlleleCountMatrix
     * \return Mean pairwise differences
     * \note Calcuated as sum over one minus site homozygosity
     *
     * This function is included via Sequence/summstats.hpp,
     * Sequence/summstats/classics.hpp or
     * Sequence/summstats/thetapi.hpp
     *
     * See \cite Tajima1983-it for details.
     * \ingroup popgenanalysis
     */
    double thetapi(const AlleleCountMatrix& ac);
} // namespace Sequence

#endif
